(function () {
  'use strict';

  var FORM_SELECTOR = '#ec-event-lead-form, #ec-event-lead-form-en, #ec-event-lead-form-es';
  var FORM_SECTION_TARGETS = ['#solicitar-orcamento', '#cotacao', '#quote', '#presupuesto'];

  function pageLanguage() {
    var lang = (document.documentElement.getAttribute('lang') || '').toLowerCase();
    if (lang.indexOf('en') === 0 || location.pathname.indexOf('/en/') === 0) return 'en';
    if (lang.indexOf('es') === 0 || location.pathname.indexOf('/es/') === 0) return 'es';
    return 'pt-BR';
  }

  function pushEvent(eventName, details) {
    var payload = {
      event: eventName,
      form_id: details.form_id,
      page_path: location.pathname,
      page_language: pageLanguage(),
      event_variant: 'events_whatsapp_quote_v1'
    };
    Object.keys(details).forEach(function (key) {
      if (key !== 'form_id') payload[key] = details[key];
    });
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
  }

  function field(form, selectors) {
    for (var i = 0; i < selectors.length; i += 1) {
      var element = form.querySelector(selectors[i]);
      if (element) return element;
    }
    return null;
  }

  function normalizeText(value) {
    return String(value || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');
  }

  function eventFormat(form) {
    var element = field(form, ['#ec-event-format', '#tipo', '[name="format"]']);
    var value = normalizeText(element && element.value);
    if (!value) return 'not_informed';
    if (/breakfast|cafe da manha|desayuno/.test(value)) return 'breakfast';
    if (/lunch|almoco|almuerzo/.test(value)) return 'lunch';
    if (/welcome/.test(value)) return 'welcome_drink';
    if (/cocktail|coquetel|coctel/.test(value)) return 'cocktail';
    if (/workshop|meeting|reuniao|reunion/.test(value)) return 'meeting_workshop';
    if (/wedding|casamento|boda|celebr/.test(value)) return 'wedding_celebration';
    if (/tour|turistic|grupo/.test(value)) return 'tour_group';
    if (/corporat|empresa|agency|agencia|brand|marca|product|produto|producto/.test(value)) return 'corporate';
    if (/other|outro|otro/.test(value)) return 'other';
    return 'other';
  }

  function guestBand(form) {
    var element = field(form, ['#ec-event-guests', '#convidados', '[name="guests"]']);
    var match = String(element && element.value || '').match(/\d+/);
    if (!match) return 'not_informed';
    var guests = parseInt(match[0], 10);
    if (guests <= 20) return '1-20';
    if (guests <= 50) return '21-50';
    if (guests <= 100) return '51-100';
    if (guests <= 150) return '101-150';
    return '151_plus';
  }

  function safeFieldKey(element) {
    var key = element && (element.getAttribute('name') || element.id) || 'unknown';
    var aliases = {
      'ec-event-name': 'name', nome: 'name', name: 'name',
      'ec-event-contact': 'contact', contact: 'contact', email: 'email', tel: 'phone',
      'ec-event-date': 'date', date: 'date', data: 'date',
      'ec-event-guests': 'guests', guests: 'guests', convidados: 'guests',
      'ec-event-format': 'event_type', format: 'event_type', tipo: 'event_type',
      empresa: 'company', msg: 'message', 'ec-event-notes': 'message', notes: 'message'
    };
    return aliases[key] || 'other';
  }

  function ctaLocation(element) {
    if (element.closest('nav')) return 'top_navigation';
    if (element.closest('header, .hero')) return 'hero';
    if (element.closest('footer')) return 'footer';
    if (element.closest('.contact, .contato, .cotacao, [id*="orcamento"]')) return 'form_section';
    return 'page_content';
  }

  function trackCtas(form) {
    document.addEventListener('click', function (event) {
      var link = event.target && event.target.closest ? event.target.closest('a') : null;
      if (!link) return;
      var href = (link.getAttribute('href') || '').toLowerCase();
      var isFormLink = FORM_SECTION_TARGETS.some(function (target) {
        return href === target || href.slice(-target.length) === target;
      });
      var isWhatsApp = href.indexOf('wa.me/') !== -1 || href.indexOf('api.whatsapp.com/') !== -1;
      var isEventEmail = href.indexOf('mailto:eventos@') === 0;
      if (!isFormLink && !isWhatsApp && !isEventEmail) return;
      pushEvent('ec_event_form_cta_click', {
        form_id: form.id,
        cta_destination: isFormLink ? 'form' : (isWhatsApp ? 'whatsapp' : 'email'),
        cta_location: ctaLocation(link)
      });
    });
  }

  function trackForm(form) {
    var started = false;
    var viewed = false;
    var invalidBatch = [];
    var invalidTimer = null;

    function markStarted() {
      if (started) return;
      started = true;
      pushEvent('ec_event_form_start', { form_id: form.id });
    }

    form.addEventListener('focusin', markStarted);
    form.addEventListener('input', markStarted);

    form.addEventListener('invalid', function (event) {
      if (invalidBatch.indexOf(event.target) === -1) invalidBatch.push(event.target);
      if (invalidTimer) return;
      invalidTimer = window.setTimeout(function () {
        var common = {
          form_id: form.id,
          event_format_group: eventFormat(form),
          guest_count_band: guestBand(form)
        };
        pushEvent('ec_event_form_submit_attempt', {
          form_id: common.form_id,
          event_format_group: common.event_format_group,
          guest_count_band: common.guest_count_band,
          form_valid: 'false'
        });
        pushEvent('ec_event_form_validation_error', {
          form_id: common.form_id,
          event_format_group: common.event_format_group,
          guest_count_band: common.guest_count_band,
          invalid_field_count: invalidBatch.length,
          first_invalid_field: safeFieldKey(invalidBatch[0])
        });
        invalidBatch = [];
        invalidTimer = null;
      }, 0);
    }, true);

    form.addEventListener('submit', function () {
      var invalidFields = Array.prototype.filter.call(
        form.querySelectorAll('input, select, textarea'),
        function (element) { return !element.validity.valid; }
      );
      var common = {
        form_id: form.id,
        event_format_group: eventFormat(form),
        guest_count_band: guestBand(form)
      };
      pushEvent('ec_event_form_submit_attempt', {
        form_id: common.form_id,
        event_format_group: common.event_format_group,
        guest_count_band: common.guest_count_band,
        form_valid: invalidFields.length === 0 ? 'true' : 'false'
      });
      if (invalidFields.length) {
        pushEvent('ec_event_form_validation_error', {
          form_id: common.form_id,
          event_format_group: common.event_format_group,
          guest_count_band: common.guest_count_band,
          invalid_field_count: invalidFields.length,
          first_invalid_field: safeFieldKey(invalidFields[0])
        });
      } else {
        pushEvent('ec_event_form_valid', common);
      }
    }, true);

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(function (entries) {
        if (!viewed && entries.some(function (entry) { return entry.isIntersecting; })) {
          viewed = true;
          pushEvent('ec_event_form_view', { form_id: form.id });
          observer.disconnect();
        }
      }, { threshold: 0.15 });
      observer.observe(form);
    } else {
      pushEvent('ec_event_form_view', { form_id: form.id });
    }
  }

  function init() {
    var form = document.querySelector(FORM_SELECTOR);
    if (!form) return;
    trackCtas(form);
    trackForm(form);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();

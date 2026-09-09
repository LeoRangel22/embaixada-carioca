from pathlib import Path
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
b=Path(sys.argv[1]);v=sys.argv[2];out=b/'output'/f'Manual-Embaixada-Carioca-{v}.pdf'
c=canvas.Canvas(str(out),pagesize=(540,960));c.setTitle(f'Manual Embaixada Carioca {v}');c.setAuthor('Embaixada Carioca')
for i in range(1,6):
 c.drawImage(ImageReader(str(b/'build'/f'slide-{i}.png')),0,0,width=540,height=960)
 c.linkURL('https://www.embaixadacarioca.com/abastecer/manual/',(0,0,540,40),relative=0)
 c.showPage()
c.save();print(out)

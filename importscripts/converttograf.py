import sys
import poioapi
from poioapi.io import typecraft, elan

p = sys.argv[1]
f = p[:-4]
parser  =  poioapi.io.elan.Parser(p)
#parser  =  poioapi.io.typecraft.Parser(p)
writer  =  poioapi.io.graf.Writer()
converter  =  poioapi.io.graf.GrAFConverter(parser,  writer)
converter.parse()
converter.write("%s.hdr"%f)
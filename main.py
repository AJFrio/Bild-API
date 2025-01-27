import bild
import dotenv
import pprint

dotenv.load_dotenv()

b = bild.Bild()

pprint.pprint(b.get_all_users())


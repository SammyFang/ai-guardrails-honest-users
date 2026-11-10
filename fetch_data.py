from pathlib import Path
import csv,hashlib,urllib.request
B=Path(__file__).resolve().parent
for r in csv.DictReader((B/'sources/fetch_manifest.csv').open(encoding='utf-8-sig')):
 p=B/r['local_path'];p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']:continue
 with urllib.request.urlopen(urllib.request.Request(r['url'],headers={'User-Agent':'PublicResearchReplication/1.0'}),timeout=90) as z:b=z.read()
 assert hashlib.sha256(b).hexdigest()==r['sha256'],f"Official bytes changed:{r['local_path']}"
 p.write_bytes(b)
print('Official public source data verified bySHA256.')

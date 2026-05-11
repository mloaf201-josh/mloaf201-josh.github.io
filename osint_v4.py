import http.server,socket,urllib.request
from urllib.parse import urlparse,parse_qs

H="""<!DOCTYPE html>
<html lang=en><head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>OSINT</title>
<style>
body{background:#050510;color:#e0e0ee;font-family:sans-serif;padding:1rem}
h1{color:#fff;font-size:1.5rem}h1 span{color:#1da1f2}
.sub{color:rgba(255,255,255,0.2);font-size:0.75rem;margin-bottom:1rem}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:0.5rem}
.card{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:0.8rem;margin-bottom:0.5rem}
.card h3{font-size:0.7rem;color:#1da1f2;margin-bottom:0.3rem}
.card input{width:100%;padding:0.4rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:4px;color:#e0e0ee;margin-bottom:0.3rem}
.card button{padding:0.3rem 0.8rem;background:linear-gradient(135deg,#1da1f2,#a855f7);border:none;border-radius:4px;color:#fff;cursor:pointer}
.res{background:rgba(0,0,0,0.2);border-radius:6px;padding:0.6rem;font-size:0.75rem;margin-top:0.4rem;min-height:2rem;white-space:pre-wrap;font-family:monospace;color:rgba(255,255,255,0.6)}
footer{text-align:center;color:rgba(255,255,255,0.04);font-size:0.6rem;margin-top:1rem}
</style></head><body>
<h1>&#x1F50D; <span>OSINT</span> Engine</h1>
<div class=sub>joshx-osint &middot; Pi 5</div>
<div class=grid>
<div class=card><h3>IP Lookup</h3><input id=t1 value=8.8.8.8><button onclick=g(1)>Query</button><div class=res id=r1></div></div>
<div class=card><h3>Port Check</h3><input id=t2 value=google.com:80><button onclick=g(2)>Scan</button><div class=res id=r2></div></div>
<div class=card><h3>HTTP Headers</h3><input id=t3 value=https://example.com><button onclick=g(3)>Fetch</button><div class=res id=r3></div></div>
<div class=card><h3>DNS Records</h3><input id=t4 value=google.com><button onclick=g(4)>Resolve</button><div class=res id=r4></div></div>
</div>
<footer>JOSH-X Security Suite</footer>
<script>
async function g(n){
 var v=document.getElementById('t'+n).value;if(!v)return;
 var o=document.getElementById('r'+n);o.textContent='.';
 try{var x=await fetch('/api?q='+encodeURIComponent(v)+'&t='+n);o.textContent=await x.text()}
 catch(e){o.textContent='Error: '+e.message}
}
</script>
</body></html>"""

class S(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        if self.path.startswith("/api"):
            q=parse_qs(urlparse(self.path).query);qry=q.get("q",[""])[0];t=q.get("t",["1"])[0];r="No result"
            try:
                if t=="1":ip=socket.gethostbyname(qry);r="Target: "+qry+"\nIP: "+ip
                elif t=="2":
                    h,p=qry.split(":") if ":" in qry else (qry,"80");s=socket.socket();s.settimeout(3)
                    r="Port "+p+": "+("OPEN" if s.connect_ex((h,int(p)))==0 else "CLOSED");s.close()
                elif t=="3":
                    u=urllib.request.urlopen(qry,timeout=5)
                    r="HTTP "+str(u.status)+"\nServer: "+u.headers.get("Server","?")+"\nContent-Type: "+u.headers.get("Content-Type","?")
                elif t=="4":
                    a=socket.getaddrinfo(qry,0,socket.AF_UNSPEC,socket.SOCK_STREAM)
                    v4=list(set(i[4][0] for i in a if i[0]==socket.AF_INET))
                    v6=list(set(i[4][0] for i in a if i[0]==socket.AF_INET6))
                    r="IPv4: "+(", ".join(v4) or "none")+"\nIPv6: "+(", ".join(v6) or "none")
            except Exception as e:r="Error: "+str(e)[:80]
            self.wfile.write(r.encode())
        else:
            self.wfile.write(H.encode())

http.server.HTTPServer(("0.0.0.0",9193),S).serve_forever()

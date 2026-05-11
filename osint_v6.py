import http.server,socket,urllib.request,json,subprocess,os
from urllib.parse import urlparse,parse_qs

H="""<!DOCTYPE html>
<html lang=en><head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>OSINT Engine</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050510;color:#e0e0ee;font-family:sans-serif;padding:1rem}
h1{color:#fff;font-size:1.5rem}h1 span{color:#1da1f2}
.sub{color:rgba(255,255,255,0.2);font-size:0.75rem;margin-bottom:1rem}
.g{display:grid;gap:0.5rem;margin-bottom:0.5rem}
.c2{grid-template-columns:1fr 1fr}.c3{grid-template-columns:1fr 1fr 1fr}
@media(max-width:700px){.c2,.c3{grid-template-columns:1fr}}
.card{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:0.8rem}
.card h3{font-size:0.7rem;color:#1da1f2;margin-bottom:0.3rem;text-transform:uppercase}
.card p{font-size:0.6rem;color:rgba(255,255,255,0.2);margin-bottom:0.4rem}
.card input{width:100%;padding:0.35rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:4px;color:#e0e0ee;margin-bottom:0.3rem;font-size:0.75rem}
.card button{padding:0.3rem 0.8rem;background:linear-gradient(135deg,#1da1f2,#a855f7);border:none;border-radius:4px;color:#fff;cursor:pointer;font-size:0.7rem}
.card .opts{display:flex;gap:0.4rem;flex-wrap:wrap;margin-bottom:0.3rem;align-items:center}
.card .opts label{font-size:0.6rem;color:rgba(255,255,255,0.3);display:flex;align-items:center;gap:0.2rem;cursor:pointer}
.card .opts input[type=checkbox]{width:auto;margin:0;accent-color:#1da1f2}
.res{background:rgba(0,0,0,0.25);border-radius:6px;padding:0.6rem;font-size:0.75rem;margin-top:0.4rem;min-height:2rem;white-space:pre-wrap;font-family:monospace;color:rgba(255,255,255,0.6);max-height:350px;overflow:auto}
.tag{font-size:0.5rem;padding:0.1rem 0.3rem;border-radius:3px;margin-left:0.3rem}
.tag.n{background:rgba(74,222,128,0.1);color:#4ade80}
.tag.d{background:rgba(250,204,21,0.1);color:#eab308}
footer{text-align:center;color:rgba(255,255,255,0.04);font-size:0.6rem;margin-top:1rem}
</style></head><body>
<h1>&#x1F50D; <span>OSINT</span> Engine</h1>
<div class=sub>joshx-osint &middot; Pi 5 &middot; People Search &middot; Network Tools</div>

<div class="g c2">
<div class=card><h3>&#x1F310; IP Lookup</h3><input id=t1 value=8.8.8.8><button onclick=g(1)>Query</button><div class=res id=r1></div></div>
<div class=card><h3>&#x1F7E2; Port Check</h3><input id=t2 value=google.com:80><button onclick=g(2)>Scan</button><div class=res id=r2></div></div>
<div class=card><h3>&#x1F4E1; HTTP Headers</h3><input id=t3 value=https://example.com><button onclick=g(3)>Fetch</button><div class=res id=r3></div></div>
<div class=card><h3>&#x1F500; DNS Records</h3><input id=t4 value=google.com><button onclick=g(4)>Resolve</button><div class=res id=r4></div></div>
</div>

<div class="g c3">
<div class=card style="border-color:rgba(74,222,128,0.15)">
<h3>&#x1F50D; Sherlock <span class="tag n">NEW</span></h3>
<p>Find username across 400+ sites</p>
<div class=opts>
<label><input type=checkbox id=c5> Print all</label>
<label><input type=checkbox id=c5b> NSFW</label>
</div>
<input id=t5 placeholder=username value=johndoe><button onclick=g(5)>Search</button>
<div class=res id=r5></div>
</div>

<div class=card style="border-color:rgba(74,222,128,0.15)">
<h3>&#x1F4E7; Holehe <span class="tag n">NEW</span></h3>
<p>Check email registration on 120+ sites</p>
<div class=opts>
<label><input type=checkbox id=c6> Only used</label>
<label><input type=checkbox id=c6b> Skip recovery</label>
</div>
<input id=t6 placeholder=email@example.com><button onclick=g(6)>Check</button>
<div class=res id=r6></div>
</div>

<div class=card style="border-color:rgba(74,222,128,0.15)">
<h3>&#x1F9F1; Maigret <span class="tag d">BETA</span></h3>
<p>Advanced username search (if installed)</p>
<div class=opts>
<label><input type=checkbox id=c7> All sites</label>
</div>
<input id=t7 placeholder=username><button onclick=g(7)>Search</button>
<div class=res id=r7></div>
</div>
</div>

<footer>JOSH-X Security Suite &middot; Built by Josh &#x1F3AF;</footer>
<script>
async function g(n){
 var v=document.getElementById('t'+n).value;if(!v)return;
 var o=document.getElementById('r'+n);o.textContent='.';
 var u='/api?q='+encodeURIComponent(v)+'&t='+n;
 for(var i=0;i<10;i++){
  var c=document.getElementById('c'+n+(i?'b'+i:''));
  if(c&&c.checked)u+='&o'+i+'=1';
 }
 try{var x=await fetch(u);o.textContent=await x.text()}
 catch(e){o.textContent='Error: '+e.message}
}
</script>
</body></html>"""

class S(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html;charset=utf-8")
        self.end_headers()
        if not self.path.startswith("/api"):
            self.wfile.write(H.encode("utf-8"));return
        q=parse_qs(urlparse(self.path).query)
        qry=q.get("q",[""])[0];t=q.get("t",["1"])[0]
        o1=q.get("o1",[""])[0];o2=q.get("o2",[""])[0];o3=q.get("o3",[""])[0];ob=q.get("ob",[""])[0]
        r="No result"
        try:
            if t=="1":
                ip=socket.gethostbyname(qry);r="Target: "+qry+"\nIP: "+ip
            elif t=="2":
                h,p=qry.split(":") if ":" in qry else (qry,"80");s=socket.socket();s.settimeout(3)
                r="Port "+p+": "+("OPEN" if s.connect_ex((h,int(p)))==0 else "CLOSED");s.close()
            elif t=="3":
                u=urllib.request.urlopen(qry,timeout=5)
                r="HTTP "+str(u.status)+"\nServer: "+u.headers.get("Server","?")+"\nCT: "+u.headers.get("Content-Type","?")
            elif t=="4":
                a=socket.getaddrinfo(qry,0,socket.AF_UNSPEC,socket.SOCK_STREAM)
                v4=list(set(i[4][0] for i in a if i[0]==socket.AF_INET))
                v6=list(set(i[4][0] for i in a if i[0]==socket.AF_INET6))
                r="IPv4: "+(", ".join(v4) or "none")+"\nIPv6: "+(", ".join(v6) or "none")
            elif t=="5":
                cmd=["python3","-m","sherlock_project",qry]
                if o1:cmd+=["--print-all"]
                if o2:cmd+=["--nsfw"]
                cmd+=["--timeout","30"]
                p=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
                r=p.stdout[:3000] or p.stderr[:300]
            elif t=="6":
                cmd=["holehe",qry]
                if o1:cmd+=["--only-used"]
                if o2:cmd+=["-NP"]
                cmd+=["-T","15"]
                p=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
                r=p.stdout[:3000] or p.stderr[:300]
            elif t=="7":
                cmd=["python3","-m","maigret",qry]
                if o1:cmd+=["--all"]
                p=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
                r=p.stdout[:3000] or p.stderr[:300]
        except subprocess.TimeoutExpired:r="Command timed out (increase timeout?)"
        except Exception as e:r="Error: "+str(e)[:100]
        self.wfile.write(r.encode("utf-8"))

http.server.HTTPServer(("0.0.0.0",9193),S).serve_forever()

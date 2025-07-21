# import os, json, re, socket, dotenv, google.generativeai as genai
# from flask import Flask, render_template, request, jsonify
# from whois import whois

# dotenv.load_dotenv()

# GEN_API_KEY = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=GEN_API_KEY)

# MODEL_NAME = "gemini-2.5-flash"
# N_SUGGESTIONS = 25

# # Enhanced style prompts with contextual sensitivity
# STYLE_PROMPTS = {
#     "default": (
#         "Generate creative, brandable domain names suitable for global businesses. "
#         "Focus on universal appeal and memorability. "
#         "Only use cultural references when they naturally fit the business concept."
#     ),
#     "moroccan": (
#         "Incorporate Moroccan/Arabic elements ONLY when contextually appropriate:"
#         "\n- Use Darija words like souk, dar, atlas ONLY for relevant businesses "
#         "(e.g., dar for housing, souk for markets)"
#         "\n- Blend cultural elements subtly (e.g., TechSouk for tech marketplace)"
#         "\n- Avoid forced cultural references that don't match the business"
#         "\nPrioritize natural integration over forced cultural terms."
#     ),
#     "professional": (
#         "Use formal terminology ONLY when suitable for the industry:"
#         "\n- Corporate terms (solutions, global) for B2B/services"
#         "\n- Simpler names for consumer apps/startups"
#         "\n- Match formality level to business type "
#         "(e.g., 'ApexVentures' for finance, 'BloomStudio' for creative agencies)"
#     ),
#     "funny": (
#         "Apply humor judiciously based on business context:"
#         "\n- Puns/wordplay for lighthearted businesses (food, pets)"
#         "\n- Avoid humor for sensitive industries (healthcare, finance)"
#         "\n- Ensure jokes enhance rather than undermine the brand"
#         "\nWhen in doubt, default to clever over crude"
#     )
# }

# # Core prompt template with contextual guidance
# PROMPT = """You are a domain naming expert. Generate exactly {n} domain suggestions for: "{idea}"

# **Style Application Rules:**
# {style_instruction}

# **Universal Requirements:**
# 1. Use ONLY these extensions: {extensions_str}
# 2. Keep names under 12 characters
# 3. Provide 2-3 alternative TLDs per domain
# 4. Apply style elements ONLY when contextually appropriate
# 5. Prioritize natural fit over forced styling

# **Response Format (JSON only):**
# [{{"domain":"example.com","alt":["example.net","example.io"]}}]
# """

# def suggest_domains(idea: str, extensions: list, style: str = "default", n: int = N_SUGGESTIONS):
#     # Get style-specific instruction
#     style_instruction = STYLE_PROMPTS.get(style, STYLE_PROMPTS["default"])

#     # Format extensions for prompt
#     extensions_str = ", ".join(extensions)

#     # Create prompt
#     prompt = PROMPT.format(
#         idea=idea.strip(),
#         n=n,
#         style_instruction=style_instruction,
#         extensions_str=extensions_str
#     )

#     try:
#         resp = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
#         text = resp.text.strip()

#         # Clean up the response
#         text = text.replace('\`\`\`json', '').replace('\`\`\`', '').strip()

#         # Find JSON array
#         match = re.search(r'\[.*\]', text, re.DOTALL)
#         if match:
#             domains = json.loads(match.group(0))
#             print(f"Successfully generated {len(domains)} domains")
#             return domains
#         else:
#             print("No JSON found in response")
#             return generate_fallback_domains(idea, extensions)

#     except Exception as e:
#         print(f"Error generating domains: {e}")
#         return generate_fallback_domains(idea, extensions)


# def generate_fallback_domains(idea, extensions):
#     base = idea.lower().replace(' ', '')
#     names = [
#         f"{base[:8]}",
#         f"my{base[:6]}",
#         f"{base[:6]}hub",
#         f"{base[:6]}pro",
#         f"get{base[:5]}",
#         f"{base[:7]}ly",
#         f"{base[:5]}ify"
#     ]

#     domains = []
#     for i, name in enumerate(names):
#         # Ensure we have at least 3 extensions
#         ext_options = extensions.copy()
#         if len(ext_options) < 3:
#             ext_options += ['.com', '.net', '.io'][:3 - len(ext_options)]

#         main_ext = ext_options[i % len(ext_options)]
#         alt_exts = [ext for ext in ext_options if ext != main_ext][:2]

#         domains.append({
#             "domain": f"{name}{main_ext}",
#             "alt": [f"{name}{ext}" for ext in alt_exts]
#         })

#     print(f"Generated {len(domains)} fallback domains")
#     return domains


# def domain_status(domain: str) -> str:
#     # WHOIS check
#     try:
#         info = whois(domain)
#         return "taken" if info.domain_name else "available"
#     except:
#         return "maybe"


# # Flask app
# app = Flask(__name__, static_folder="static", template_folder="templates")


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/api/suggest", methods=["POST"])
# def api_suggest():
#     data = request.get_json(force=True)
#     idea = data.get("idea", "")
#     style = data.get("style", "default")
#     extensions = data.get("extensions", [])

#     print(f"Generating domains for: '{idea}' (Style: {style}, Extensions: {extensions})")

#     raw = suggest_domains(idea, extensions, style)

#     print(f"\n=== DOMAIN GENERATION DEBUG ===")
#     print(f"Generated {len(raw)} raw domains")

#     checked = []
#     for s in raw:
#         s["status"] = domain_status(s["domain"])
#         if s["status"] != "taken":
#             checked.append(s)
#             print(f"✓ {s['domain']} ({s['status']}) - alt: {s['alt']}")
#         else:
#             print(f"✗ {s['domain']} (taken)")

#     print(f"Returning {len(checked)} available domains")
#     print("=== END DEBUG ===\n")

#     return jsonify(checked)


# if __name__ == "__main__":
#     app.run(debug=True, port=int(os.getenv("PORT", 5000)))




# 22222


# import os, json, re, requests, dotenv, google.generativeai as genai
# from flask import Flask, render_template, request, jsonify

# dotenv.load_dotenv()

# GEN_API_KEY = os.getenv("GEMINI_API_KEY")
# DR_CLIENT   = os.getenv("DOMAINR_CLIENT_ID")
# DR_SECRET   = os.getenv("DOMAINR_CLIENT_SECRET")

# genai.configure(api_key=GEN_API_KEY)

# MODEL_NAME = "gemini-2.5-flash"
# N_SUGGESTIONS = 12

# # COMPLETELY NEW APPROACH: Force AI to generate specific extensions
# PROMPT = """You are a domain naming expert. Generate exactly {n} domain suggestions for this business idea: "{idea}"

# CRITICAL REQUIREMENTS:
# 1. Generate domains with THESE EXACT extensions in this order:
#    - 3 domains ending with .com
#    - 2 domains ending with .ma  
#    - 2 domains ending with .net
#    - 2 domains ending with .org
#    - 1 domain ending with .info
#    - 1 domain ending with .me
#    - 1 domain ending with .net.ma

# 2. Use Moroccan/Arabic-inspired names when appropriate (souk, bzaf, dar, atlas, etc.)
# 3. Keep domain names under 12 characters before the extension
# 4. Each domain should be unique and creative

# RESPONSE FORMAT (JSON only):
# [
#   {{"domain":"example.com","alt":["example.ma","example.net"]}},
#   {{"domain":"soukbiz.com","alt":["soukbiz.org","soukbiz.info"]}},
#   {{"domain":"darweb.com","alt":["darweb.ma","darweb.me"]}},
#   {{"domain":"biznes.ma","alt":["biznes.com","biznes.net"]}},
#   {{"domain":"atlas.ma","alt":["atlas.org","atlas.info"]}},
#   {{"domain":"websouk.net","alt":["websouk.com","websouk.ma"]}},
#   {{"domain":"digital.net","alt":["digital.org","digital.me"]}},
#   {{"domain":"startup.org","alt":["startup.com","startup.info"]}},
#   {{"domain":"business.org","alt":["business.net","business.ma"]}},
#   {{"domain":"services.info","alt":["services.com","services.net"]}},
#   {{"domain":"online.me","alt":["online.org","online.ma"]}},
#   {{"domain":"web.net.ma","alt":["web.com","web.ma"]}}
# ]

# Generate exactly this structure with {n} domains total."""

# def suggest_domains(idea: str, n: int = N_SUGGESTIONS):
#     prompt = PROMPT.format(idea=idea.strip(), n=n)
    
#     try:
#         resp = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
#         text = resp.text.strip()
        
#         # Clean up the response
#         text = text.replace('\`\`\`json', '').replace('\`\`\`', '').strip()
        
#         # Find JSON array
#         match = re.search(r'\[.*\]', text, re.DOTALL)
#         if match:
#             domains = json.loads(match.group(0))
#             print(f"Successfully generated {len(domains)} domains")
#             for domain in domains[:5]:  # Print first 5 for debugging
#                 print(f"  - {domain['domain']}")
#             return domains
#         else:
#             print("No JSON found in response:", text[:200])
#             return generate_fallback_domains(idea)
            
#     except Exception as e:
#         print(f"Error generating domains: {e}")
#         return generate_fallback_domains(idea)

# def generate_fallback_domains(idea):
#     """Generate fallback domains if AI fails"""
#     base_names = [
#         f"{idea.lower()[:8]}",
#         f"my{idea.lower()[:6]}",
#         f"{idea.lower()[:6]}web",
#         f"{idea.lower()[:6]}pro",
#         f"dar{idea.lower()[:5]}",
#         f"souk{idea.lower()[:4]}",
#         f"{idea.lower()[:5]}ma",
#         f"atlas{idea.lower()[:3]}",
#         f"{idea.lower()[:7]}24",
#         f"web{idea.lower()[:5]}",
#         f"{idea.lower()[:6]}net",
#         f"digital{idea.lower()[:2]}"
#     ]
    
#     extensions = ['.com', '.ma', '.net', '.org', '.info', '.me', '.net.ma', '.co.ma', '.org.ma', '.press.ma', '.gov.ma', '.ac.ma']
    
#     domains = []
#     for i, base in enumerate(base_names):
#         main_ext = extensions[i % len(extensions)]
#         alt_exts = [ext for ext in extensions[:4] if ext != main_ext][:2]
        
#         domains.append({
#             "domain": f"{base}{main_ext}",
#             "alt": [f"{base}{ext}" for ext in alt_exts]
#         })
    
#     print(f"Generated {len(domains)} fallback domains")
#     return domains

# # ---- Domainr availability ----
# DOMAINR_URL = "https://api.domainr.com/v2/status"

# def domain_status(domain: str) -> str:
#     """Return 'available', 'taken', or 'maybe' (if uncertain)."""
#     if not DR_CLIENT:
#         return "maybe"
    
#     params = {"domain": domain, "client_id": DR_CLIENT, "client_secret": DR_SECRET}
#     try:
#         data = requests.get(DOMAINR_URL, params=params, timeout=4).json()
#         code = data["status"][0]["status"]
#         if code.startswith("undelegated"):
#             return "available"
#         if code.startswith("inactive"):
#             return "maybe"
#         return "taken"
#     except Exception as e:
#         print(f"Domain status check error for {domain}: {e}")
#         return "maybe"

# # ---- Flask ----
# app = Flask(__name__, static_folder="static", template_folder="templates")

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/api/suggest", methods=["POST"])
# def api_suggest():
#     idea = request.get_json(force=True).get("idea", "")
#     raw = suggest_domains(idea)
    
#     print(f"\n=== DOMAIN GENERATION DEBUG ===")
#     print(f"Generated {len(raw)} raw domains")
    
#     checked = []
#     for s in raw:
#         s["status"] = domain_status(s["domain"])
#         if s["status"] != "taken":
#             checked.append(s)
#             print(f"✓ {s['domain']} ({s['status']}) - alt: {s['alt']}")
#         else:
#             print(f"✗ {s['domain']} (taken)")
    
#     print(f"Returning {len(checked)} available domains")
#     print("=== END DEBUG ===\n")
    
#     return jsonify(checked)

# if __name__ == "__main__":
#     app.run(debug=True, port=int(os.getenv("PORT", 5000)))






# # 444
# import os, json, re, requests, dotenv, google.generativeai as genai
# from flask import Flask, render_template, request, jsonify

# dotenv.load_dotenv()

# GEN_API_KEY = os.getenv("GEMINI_API_KEY")
# DR_CLIENT   = os.getenv("DOMAINR_CLIENT_ID")
# DR_SECRET   = os.getenv("DOMAINR_CLIENT_SECRET")

# genai.configure(api_key=GEN_API_KEY)

# MODEL_NAME = "gemini-2.5-flash"
# N_SUGGESTIONS = 10 # Reduced slightly to encourage focus on quality

# # Enhanced style prompts with contextual sensitivity
# STYLE_PROMPTS = {
#     "default": (
#         "Generate creative, brandable domain names suitable for global businesses. "
#         "Focus on universal appeal and memorability. "
#         "Only use cultural references when they naturally fit the business concept."
#     ),
#     "moroccan": (
#         "CRITICAL: Generate domain names that strongly reflect Moroccan culture and language. "
#         "Use authentic Moroccan Darija vocabulary or Arabic-Latin transliterations. "
#         "Blend these naturally with the business idea. "
#         "Examples of Moroccan-style domains: 'SoukOnline.ma', 'DarTech.com', 'BzafShop.net', 'AtlasVoyage.ma', 'SahaFood.org'. "
#         "Prioritize names that sound genuinely Moroccan and are easy to pronounce internationally. "
#         "Avoid generic English names unless they are combined with a strong Moroccan element."
#     ),
#     "professional": (
#         "Use formal terminology ONLY when suitable for the industry:"
#         "\n- Corporate terms (solutions, global) for B2B/services"
#         "\n- Simpler names for consumer apps/startups"
#         "\n- Match formality level to business type "
#         "(e.g., 'ApexVentures' for finance, 'BloomStudio' for creative agencies)"
#     ),
#     "funny": (
#         "Apply humor judiciously based on business context:"
#         "\n- Puns/wordplay for lighthearted businesses (food, pets)"
#         "\n- Avoid humor for sensitive industries (healthcare, finance)"
#         "\n- Ensure jokes enhance rather than undermine the brand"
#         "\nWhen in doubt, default to clever over crude"
#     )
# }

# # Enhanced prompt template with style and extension flexibility
# PROMPT = """You are a domain naming expert. Generate exactly {n} domain suggestions for: "{idea}"

# **Style Application Rules:**
# {style_instruction}

# **Extension Requirements:**
# 1. Use ONLY these extensions: {extensions_str}
# 2. Distribute domains across the selected extensions
# 3. Prioritize .com and .ma when available

# **Universal Requirements:**
# 1. Keep names under 12 characters before the extension
# 2. Provide 2-3 alternative extensions per domain
# 3. Apply style elements ONLY when contextually appropriate
# 4. Prioritize natural fit over forced styling
# 5. Each domain should be unique and creative

# **Response Format (JSON only):**
# [
#   {{"domain":"example.com","alt":["example.ma","example.net"]}},
#   {{"domain":"soukbiz.ma","alt":["soukbiz.com","soukbiz.org"]}},
#   {{"domain":"webpro.net","alt":["webpro.com","webpro.info"]}}
# ]

# Generate exactly {n} domains total."""

# def suggest_domains(idea: str, extensions: list = None, style: str = "default", n: int = N_SUGGESTIONS):
#     # Default extensions if none provided
#     if not extensions:
#         extensions = ['.com', '.ma', '.net', '.org', '.info', '.me', '.net.ma']
    
#     # Get style-specific instruction
#     style_instruction = STYLE_PROMPTS.get(style, STYLE_PROMPTS["default"])
    
#     # Format extensions for prompt
#     extensions_str = ", ".join(extensions)
    
#     # Create prompt
#     prompt = PROMPT.format(
#         idea=idea.strip(),
#         n=n,
#         style_instruction=style_instruction,
#         extensions_str=extensions_str
#     )
    
#     try:
#         resp = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
#         text = resp.text.strip()
        
#         # Clean up the response
#         text = text.replace('\`\`\`json', '').replace('\`\`\`', '').strip()
        
#         # Find JSON array
#         match = re.search(r'\[.*\]', text, re.DOTALL)
#         if match:
#             domains = json.loads(match.group(0))
#             print(f"Successfully generated {len(domains)} domains with {style} style")
#             for domain in domains[:5]:  # Print first 5 for debugging
#                 print(f"  - {domain['domain']}")
#             return domains
#         else:
#             print("No JSON found in response:", text[:200])
#             return generate_fallback_domains(idea, extensions)
            
#     except Exception as e:
#         print(f"Error generating domains: {e}")
#         return generate_fallback_domains(idea, extensions)

# def generate_fallback_domains(idea, extensions=None):
#     """Generate fallback domains if AI fails"""
#     if not extensions:
#         extensions = ['.com', '.ma', '.net', '.org', '.info', '.me', '.net.ma', '.co.ma', '.org.ma', '.press.ma', '.gov.ma', '.ac.ma']
    
#     base_names = [
#         f"{idea.lower()[:8]}",
#         f"my{idea.lower()[:6]}",
#         f"{idea.lower()[:6]}web",
#         f"{idea.lower()[:6]}pro",
#         f"dar{idea.lower()[:5]}",
#         f"souk{idea.lower()[:4]}",
#         f"{idea.lower()[:5]}ma",
#         f"atlas{idea.lower()[:3]}",
#         f"{idea.lower()[:7]}24",
#         f"web{idea.lower()[:5]}",
#         f"{idea.lower()[:6]}net",
#         f"digital{idea.lower()[:2]}"
#     ]
    
#     domains = []
#     for i, base in enumerate(base_names):
#         main_ext = extensions[i % len(extensions)]
#         alt_exts = [ext for ext in extensions[:4] if ext != main_ext][:2]
        
#         domains.append({
#             "domain": f"{base}{main_ext}",
#             "alt": [f"{base}{ext}" for ext in alt_exts]
#         })
    
#     print(f"Generated {len(domains)} fallback domains")
#     return domains

# # ---- Domainr availability ----
# DOMAINR_URL = "https://api.domainr.com/v2/status"

# def domain_status(domain: str) -> str:
#     """Return 'available', 'taken', or 'maybe' (if uncertain)."""
#     if not DR_CLIENT:
#         return "maybe"
    
#     params = {"domain": domain, "client_id": DR_CLIENT, "client_secret": DR_SECRET}
#     try:
#         data = requests.get(DOMAINR_URL, params=params, timeout=4).json()
#         code = data["status"][0]["status"]
#         if code.startswith("undelegated"):
#             return "available"
#         if code.startswith("inactive"):
#             return "maybe"
#         return "taken"
#     except Exception as e:
#         print(f"Domain status check error for {domain}: {e}")
#         return "maybe"

# # ---- Flask ----
# app = Flask(__name__, static_folder="static", template_folder="templates")

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/api/suggest", methods=["POST"])
# def api_suggest():
#     data = request.get_json(force=True)
#     idea = data.get("idea", "")
#     style = data.get("style", "default")
#     extensions = data.get("extensions", [])
    
#     # Convert extension format if needed (remove dots if present)
#     if extensions:
#         extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    
#     print(f"Generating domains for: '{idea}' (Style: {style}, Extensions: {extensions})")
    
#     raw = suggest_domains(idea, extensions, style)
    
#     print(f"\n=== DOMAIN GENERATION DEBUG ===")
#     print(f"Generated {len(raw)} raw domains")
    
#     checked = []
#     for s in raw:
#         s["status"] = domain_status(s["domain"])
#         if s["status"] != "taken":
#             checked.append(s)
#             print(f"✓ {s['domain']} ({s['status']}) - alt: {s['alt']}")
#         else:
#             print(f"✗ {s['domain']} (taken)")
    
#     print(f"Returning {len(checked)} available domains")
#     print("=== END DEBUG ===\n")
    
#     return jsonify(checked)

# if __name__ == "__main__":
#     app.run(debug=True, port=int(os.getenv("PORT", 5000)))


# # deepseek
# import os, json, re, dotenv, google.generativeai as genai
# from flask import Flask, render_template, request, jsonify

# dotenv.load_dotenv()

# GEN_API_KEY = os.getenv("GEMINI_API_KEY")

# genai.configure(api_key=GEN_API_KEY)

# MODEL_NAME = "gemini-2.5-flash"
# N_SUGGESTIONS = 10 # Reduced slightly to encourage focus on quality

# # Enhanced style prompts with contextual sensitivity
# STYLE_PROMPTS = {
#     "default": (
#         "Generate creative, brandable domain names suitable for global businesses. "
#         "Focus on universal appeal and memorability. "
#         "Only use cultural references when they naturally fit the business concept."
#     ),
#     "moroccan": (
#         "CRITICAL: Generate domain names that strongly reflect Moroccan culture and language. "
#         "Use authentic Moroccan Darija vocabulary or Arabic-Latin transliterations. "
#         "Blend these naturally with the business idea. "
#         "Examples of Moroccan-style domains: 'SoukOnline.ma', 'DarTech.com', 'BzafShop.net', 'AtlasVoyage.ma', 'SahaFood.org'. "
#         "Prioritize names that sound genuinely Moroccan and are easy to pronounce internationally. "
#         "Avoid generic English names unless they are combined with a strong Moroccan element."
#     ),
#     "professional": (
#         "Use formal terminology ONLY when suitable for the industry:"
#         "\n- Corporate terms (solutions, global) for B2B/services"
#         "\n- Simpler names for consumer apps/startups"
#         "\n- Match formality level to business type "
#         "(e.g., 'ApexVentures' for finance, 'BloomStudio' for creative agencies)"
#     ),
#     "funny": (
#         "Apply humor judiciously based on business context:"
#         "\n- Puns/wordplay for lighthearted businesses (food, pets)"
#         "\n- Avoid humor for sensitive industries (healthcare, finance)"
#         "\n- Ensure jokes enhance rather than undermine the brand"
#         "\nWhen in doubt, default to clever over crude"
#     )
# }

# # Enhanced prompt template with style and extension flexibility
# PROMPT = """You are a domain naming expert. Generate exactly {n} domain suggestions for: "{idea}"

# **Style Application Rules:**
# {style_instruction}

# **Extension Requirements:**
# 1. Use ONLY these extensions: {extensions_str}
# 2. Distribute domains across the selected extensions
# 3. Prioritize .com and .ma when available

# **Universal Requirements:**
# 1. Keep names under 12 characters before the extension
# 2. Provide 2-3 alternative extensions per domain
# 3. Apply style elements ONLY when contextually appropriate
# 4. Prioritize natural fit over forced styling
# 5. Each domain should be unique and creative

# **Response Format (JSON only):**
# [
#   {{"domain":"example.com","alt":["example.ma","example.net"]}},
#   {{"domain":"soukbiz.ma","alt":["soukbiz.com","soukbiz.org"]}},
#   {{"domain":"webpro.net","alt":["webpro.com","webpro.info"]}}
# ]

# Generate exactly {n} domains total."""

# def suggest_domains(idea: str, extensions: list = None, style: str = "default", n: int = N_SUGGESTIONS):
#     # Default extensions if none provided
#     if not extensions:
#         extensions = ['.com', '.ma', '.net', '.org', '.info', '.me', '.net.ma']
    
#     # Get style-specific instruction
#     style_instruction = STYLE_PROMPTS.get(style, STYLE_PROMPTS["default"])
    
#     # Format extensions for prompt
#     extensions_str = ", ".join(extensions)
    
#     # Create prompt
#     prompt = PROMPT.format(
#         idea=idea.strip(),
#         n=n,
#         style_instruction=style_instruction,
#         extensions_str=extensions_str
#     )
    
#     try:
#         resp = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
#         text = resp.text.strip()
        
#         # Clean up the response
#         text = text.replace('\`\`\`json', '').replace('\`\`\`', '').strip()
        
#         # Find JSON array
#         match = re.search(r'\[.*\]', text, re.DOTALL)
#         if match:
#             domains = json.loads(match.group(0))
#             print(f"Successfully generated {len(domains)} domains with {style} style")
#             for domain in domains[:5]:  # Print first 5 for debugging
#                 print(f"  - {domain['domain']}")
#             return domains
#         else:
#             print("No JSON found in response:", text[:200])
#             return generate_fallback_domains(idea, extensions)
            
#     except Exception as e:
#         print(f"Error generating domains: {e}")
#         return generate_fallback_domains(idea, extensions)

# def generate_fallback_domains(idea, extensions=None):
#     """Generate fallback domains if AI fails"""
#     if not extensions:
#         extensions = ['.com', '.ma', '.net', '.org', '.info', '.me', '.net.ma', '.co.ma', '.org.ma', '.press.ma', '.gov.ma', '.ac.ma']
    
#     base_names = [
#         f"{idea.lower()[:8]}",
#         f"my{idea.lower()[:6]}",
#         f"{idea.lower()[:6]}web",
#         f"{idea.lower()[:6]}pro",
#         f"dar{idea.lower()[:5]}",
#         f"souk{idea.lower()[:4]}",
#         f"{idea.lower()[:5]}ma",
#         f"atlas{idea.lower()[:3]}",
#         f"{idea.lower()[:7]}24",
#         f"web{idea.lower()[:5]}",
#         f"{idea.lower()[:6]}net",
#         f"digital{idea.lower()[:2]}"
#     ]
    
#     domains = []
#     for i, base in enumerate(base_names):
#         main_ext = extensions[i % len(extensions)]
#         alt_exts = [ext for ext in extensions[:4] if ext != main_ext][:2]
        
#         domains.append({
#             "domain": f"{base}{main_ext}",
#             "alt": [f"{base}{ext}" for ext in alt_exts]
#         })
    
#     print(f"Generated {len(domains)} fallback domains")
#     return domains

# # ---- Flask ----
# app = Flask(__name__, static_folder="static", template_folder="templates")

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/api/suggest", methods=["POST"])
# def api_suggest():
#     data = request.get_json(force=True)
#     idea = data.get("idea", "")
#     style = data.get("style", "default")
#     extensions = data.get("extensions", [])
    
#     # Convert extension format if needed (remove dots if present)
#     if extensions:
#         extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    
#     print(f"Generating domains for: '{idea}' (Style: {style}, Extensions: {extensions})")
    
#     raw = suggest_domains(idea, extensions, style)
    
#     print(f"\n=== DOMAIN GENERATION DEBUG ===")
#     print(f"Generated {len(raw)} raw domains")
    
#     # Since we removed Domainr checks, mark all domains as "maybe" available
#     checked = []
#     for s in raw:
#         s["status"] = "maybe"
#         checked.append(s)
#         print(f"? {s['domain']} (status unknown) - alt: {s['alt']}")
    
#     print(f"Returning {len(checked)} domains")
#     print("=== END DEBUG ===\n")
    
#     return jsonify(checked)

# if __name__ == "__main__":
#     app.run(debug=True, port=int(os.getenv("PORT", 5000)))



# chatgpt
# deepseek
import os, json, re, dotenv, google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import whois

dotenv.load_dotenv()

GEN_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEN_API_KEY)

MODEL_NAME = "gemini-2.5-flash"
N_SUGGESTIONS = 30

# Style prompts
STYLE_PROMPTS = {
    "default": (
        "Generate creative, brandable domain names suitable for global businesses. "
        "Focus on universal appeal and memorability. "
        "Only use cultural references when they naturally fit the business concept."
    ),
    "moroccan": (
        "CRITICAL: Generate domain names that strongly reflect Moroccan culture and language. "
        "Use authentic Moroccan Darija vocabulary or Arabic-Latin transliterations. "
        "Blend these naturally with the business idea. "
        "Examples of Moroccan-style domains: 'SoukOnline.ma', 'DarTech.com', 'BzafShop.net', 'AtlasVoyage.ma', 'SahaFood.org'. "
        "Prioritize names that sound genuinely Moroccan and are easy to pronounce internationally. "
        "Avoid generic English names unless they are combined with a strong Moroccan element."
    ),
    "professional": (
        "Use formal terminology ONLY when suitable for the industry:"
        "\n- Corporate terms (solutions, global) for B2B/services"
        "\n- Simpler names for consumer apps/startups"
        "\n- Match formality level to business type "
        "(e.g., 'ApexVentures' for finance, 'BloomStudio' for creative agencies)"
    ),
    "funny": (
        "Apply humor judiciously based on business context:"
        "\n- Puns/wordplay for lighthearted businesses (food, pets)"
        "\n- Avoid humor for sensitive industries (healthcare, finance)"
        "\n- Ensure jokes enhance rather than undermine the brand"
        "\nWhen in doubt, default to clever over crude"
    )
}

PROMPT = """You are a domain naming expert. Generate exactly {n} domain suggestions for: "{idea}"

**Style Application Rules:**
{style_instruction}

**Extension Requirements:**
1. Use ONLY these extensions: {extensions_str}
2. Distribute domains across the selected extensions
3. Prioritize .com and .ma when available

**Universal Requirements:**
1. Keep names under 12 characters before the extension
2. Provide 2-3 alternative extensions per domain
3. Apply style elements ONLY when contextually appropriate
4. Prioritize natural fit over forced styling
5. Each domain should be unique and creative

**Response Format (JSON only):**
[
  {{"domain":"example.com","alt":["example.ma","example.net"]}},
  {{"domain":"soukbiz.ma","alt":["soukbiz.com","soukbiz.org"]}},
  {{"domain":"webpro.net","alt":["webpro.com","webpro.info"]}}
]

Generate exactly {n} domains total.
"""

def is_domain_available(domain: str) -> bool:
    """
    Returns True if domain is available (not registered), False otherwise.
    """
    try:
        w = whois.whois(domain)
        return all(not w.get(field) for field in ["domain_name", "creation_date", "expiration_date", "updated_date"])
    except Exception as e:
        if "No match" in str(e) or "NOT FOUND" in str(e).upper():
            return True
        return False

def suggest_domains(idea: str, extensions: list = None, style: str = "default", n: int = N_SUGGESTIONS):
    if not extensions:
        extensions = ['.com', '.ma', '.net', '.org', '.info', '.me', '.net.ma']
    
    style_instruction = STYLE_PROMPTS.get(style, STYLE_PROMPTS["default"])
    extensions_str = ", ".join(extensions)
    
    prompt = PROMPT.format(
        idea=idea.strip(),
        n=n,
        style_instruction=style_instruction,
        extensions_str=extensions_str
    )
    
    try:
        resp = genai.GenerativeModel(MODEL_NAME).generate_content(prompt)
        text = resp.text.strip()
        text = text.replace('```json', '').replace('```', '').strip()
        
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            domains = json.loads(match.group(0))
            print(f"Successfully generated {len(domains)} domains with {style} style")
            return domains
        else:
            print("No JSON found in response:", text[:200])
            return generate_fallback_domains(idea, extensions)
            
    except Exception as e:
        print(f"Error generating domains: {e}")
        return generate_fallback_domains(idea, extensions)

def generate_fallback_domains(idea, extensions=None):
    if not extensions:
        extensions = ['.com', '.ma', '.net', '.org', '.info', '.me', '.net.ma', '.co.ma', '.org.ma', '.press.ma', '.gov.ma', '.ac.ma']
    
    base_names = [
        f"{idea.lower()[:8]}",
        f"my{idea.lower()[:6]}",
        f"{idea.lower()[:6]}web",
        f"{idea.lower()[:6]}pro",
        f"dar{idea.lower()[:5]}",
        f"souk{idea.lower()[:4]}",
        f"{idea.lower()[:5]}ma",
        f"atlas{idea.lower()[:3]}",
        f"{idea.lower()[:7]}24",
        f"web{idea.lower()[:5]}",
        f"{idea.lower()[:6]}net",
        f"digital{idea.lower()[:2]}"
    ]
    
    domains = []
    for i, base in enumerate(base_names):
        main_ext = extensions[i % len(extensions)]
        alt_exts = [ext for ext in extensions[:4] if ext != main_ext][:2]
        domains.append({
            "domain": f"{base}{main_ext}",
            "alt": [f"{base}{ext}" for ext in alt_exts]
        })
    
    print(f"Generated {len(domains)} fallback domains")
    return domains

# ---- Flask ----
app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/suggest", methods=["POST"])
def api_suggest():
    data = request.get_json(force=True)
    idea = data.get("idea", "")
    style = data.get("style", "default")
    extensions = data.get("extensions", [])
    
    if extensions:
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    
    print(f"Generating domains for: '{idea}' (Style: {style}, Extensions: {extensions})")
    
    raw = suggest_domains(idea, extensions, style)
    
    print(f"\n=== DOMAIN GENERATION DEBUG ===")
    print(f"Generated {len(raw)} raw domains")

    checked = []
    for s in raw:
        domain_main = s["domain"]
        if is_domain_available(domain_main):
            s["status"] = "available"
            checked.append(s)
            print(f"✔️ {domain_main} is available - alt: {s['alt']}")
        else:
            print(f"❌ {domain_main} is taken, skipping...")

    print(f"Returning {len(checked)} domains")
    print("=== END DEBUG ===\n")
    
    return jsonify(checked)

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))

def get_response(query, city, language, provider, api_key=None):
    """
    STUB/MOCK FUNCTION - Frontend-only interface.
    No actual AI logic, Ollama, Gemini, OpenAI, or RAG models are integrated here.
    
    Arguments:
        query (str): The prompt, planner, or festival question.
        city (str): Selected destination (e.g. Hyderabad, Varanasi, Jaipur).
        language (str): Target translation language (en, te, hi).
        provider (str): AI provider selected (Gemini, Ollama, OpenAI).
        api_key (str): Optional API key.
        
    Returns:
        dict: {
            "answer": str (itinerary or festival explanation/etiquette),
            "phrases": list (useful local phrases),
            "budget": dict (category-wise percentage breakdown)
        }
    """
    city_str = str(city).lower()
    
    # Check if city name matches Hyderabad, Varanasi, or Jaipur (supporting multiple languages)
    is_hyd = "hyderabad" in city_str or "హైదరాబాద్" in city_str or "हैदराबाद" in city_str
    is_var = "varanasi" in city_str or "వారణాసి" in city_str or "वाराणसी" in city_str
    is_jai = "jaipur" in city_str or "జైపూర్" in city_str or "जयपुर" in city_str
    
    if is_hyd:
        city_name_local = "హైదరాబాద్" if language == "te" else ("हैदराबाद" if language == "hi" else "Hyderabad")
    elif is_var:
        city_name_local = "వారణాసి" if language == "te" else ("वाराणसी" if language == "hi" else "Varanasi")
    elif is_jai:
        city_name_local = "జైపూర్" if language == "te" else ("जयपुर" if language == "hi" else "Jaipur")
    else:
        city_name_local = city

    # 1. Handle itinerary queries
    if "itinerary" in query.lower() or "days" in query.lower() or "రోజుల" in query.lower() or "दिनों" in query.lower():
        if language == "hi":
            answer = (
                f"### 🗺️ AI-जनित यात्रा कार्यक्रम: **{city_name_local}** (प्रदाता: {provider})\n\n"
                f"यहाँ आपकी प्राथमिकताओं के आधार पर तैयार किया गया यात्रा कार्यक्रम है:\n\n"
                f"#### 🌅 दिन 1: ऐतिहासिक स्थल और विरासत\n"
                f"- **सुबह**: {city_name_local} के प्रमुख ऐतिहासिक स्थलों का भ्रमण करें। प्रमुख धरोहरों को देखें और तस्वीरें लें।\n"
                f"- **दोपहर**: प्रसिद्ध स्थानीय व्यंजनों का स्वाद लें और किसी ऐतिहासिक संग्रहालय का दौरा करें।\n"
                f"- **शाम**: सांस्कृतिक कार्यक्रमों या स्थानीय झील/नदी के किनारे सुंदर शाम की सैर का आनंद लें।\n\n"
                f"#### 🎨 दिन 2: स्थानीय कला और सांस्कृतिक अनुभव\n"
                f"- **सुबह**: पारंपरिक बाजारों का दौरा करें और स्थानीय हथकरघा कारीगरों को काम करते हुए देखें।\n"
                f"- **दोपहर**: स्थानीय समुदाय के साथ दोपहर के स्वादिष्ट भोजन का आनंद लें और मिट्टी के शिल्प कार्यशाला में भाग लें।\n"
                f"- **शाम**: सुंदर सूर्यास्त का आनंद लें और पारंपरिक व्यंजनों के ढाबों पर समय बिताएं।\n\n"
                f"#### 🛍️ दिन 3: ख़रीदारी और विदाई\n"
                f"- **सुबह**: प्रसिद्ध बाज़ारों से हस्तशिल्प वस्तुएं और उपहार खरीदें।\n"
                f"- **दोपहर**: एक शांत बगीचे या स्थानीय कैफ़े में बैठकर अपने अनुभवों को लिखें।\n"
                f"- **शाम**: विशेष विदाई रात्रिभोज के साथ अपनी यात्रा का समापन करें।"
            )
        elif language == "te":
            answer = (
                f"### 🗺️ AI సృష్టించిన ప్రయాణ ప్రణాళిక: **{city_name_local}** (ప్రొవైడర్: {provider})\n\n"
                f"మీ ప్రాధాన్యతలకు అనుగుణంగా రూపొందించబడిన ప్రయాణ ప్రణాళిక ఇక్కడ ఉంది:\n\n"
                f"#### 🌅 రోజు 1: చారిత్రక అద్భుతాలు & వారసత్వం\n"
                f"- **ఉదయం**: {city_name_local} లోని ప్రధాన చారిత్రక మరియు సాంస్కృతిక ప్రదేశాలను సందర్శించండి.\n"
                f"- **మధ్యాహ్నం**: రుచికరమైన స్థానిక వంటకాలను ఆస్వాదించండి మరియు చారిత్రక మ్యూజియంను సందర్శించండి.\n"
                f"- **సాయంత్రం**: లైట్ అండ్ సౌండ్ షో లేదా హాయిగా పడవ ప్రయాణం చేయండి.\n\n"
                f"#### 🎨 రోజు 2: స్థానిక సంస్కృతి & కళలు\n"
                f"- **ఉదయం**: సాంప్రదాయ చేనేత మార్కెట్లను సందర్శించండి, స్థానిక హస్తకళాకారులను కలవండి.\n"
                f"- **మధ్యాహ్నం**: స్థానిక భోజనం ఆస్వాదించి, స్థానిక సంప్రదాయ చేతిపనుల తయారీని గమనించండి.\n"
                f"- **సాయంత్రం**: చారిత్రక వ్యూ పాయింట్ నుండి సూర్యాస్తమయాన్ని ఆస్వాదిస్తూ ఆహ్లాదంగా గడపండి.\n\n"
                f"#### 🛍️ రోజు 3: షాపింగ్ & ముగింపు\n"
                f"- **ఉదయం**: బజార్ల నుండి స్థానిక హస్తకళలు మరియు జ్ఞాపికలను కొనుగోలు చేయండి.\n"
                f"- **మధ్యాహ్నం**: ప్రశాంతమైన ఉద్యానవనంలో లేదా కేఫ్‌లో విశ్రాంతి తీసుకోండి.\n"
                f"- **సాయంత్రం**: ప్రత్యేక విందుతో ప్రయాణాన్ని ముగించండి."
            )
        else:
            answer = (
                f"### 🗺️ AI-Generated Itinerary for **{city_name_local}** (Provider: {provider})\n\n"
                f"Here is a curated itinerary tailored for you:\n\n"
                f"#### 🌅 Day 1: Historical Wonders & Heritage\n"
                f"- **Morning**: Explore the primary historical sites in {city_name_local}.\n"
                f"- **Afternoon**: Delight in local traditional street food and visit an archive/museum.\n"
                f"- **Evening**: Attend a scenic light-and-sound show or stroll around a local water body.\n\n"
                f"#### 🎨 Day 2: Artisanal Culture & Local Life\n"
                f"- **Morning**: Wander through traditional markets, watch local weavers or craftsmen at work.\n"
                f"- **Afternoon**: Enjoy a slow, authentic community lunch.\n"
                f"- **Evening**: Capture stunning sunset views from a historic viewpoint.\n\n"
                f"#### 🛍️ Day 3: Leisure & Shopping\n"
                f"- **Morning**: Pick up local souvenirs and handcrafts from bazaar areas.\n"
                f"- **Afternoon**: Relax at a peaceful garden or cafe.\n"
                f"- **Evening**: Farewell dinner at a specialty restaurant."
            )
            
    # 2. Handle festival queries
    elif "festival" in query.lower() or "పండుగ" in query.lower() or "त्योहार" in query.lower():
        fest_name = query.split(":")[-1].strip() if ":" in query else "Festival"
        
        # Translate festival names in title
        fest_display = fest_name
        if "bonalu" in fest_name.lower() or "బోనాలు" in fest_name or "बोनालु" in fest_name:
            fest_display = "బోనాలు" if language == "te" else ("बोनालु" if language == "hi" else "Bonalu")
        elif "diwali" in fest_name.lower() or "దీపావళి" in fest_name or "दीपावली" in fest_name or "दिवाली" in fest_name:
            fest_display = "దీపావళి" if language == "te" else ("दीपावली" if language == "hi" else "Diwali")
        elif "teej" in fest_name.lower() or "తీజ్" in fest_name or "तीज" in fest_name:
            fest_display = "తీజ్" if language == "te" else ("तीज" if language == "hi" else "Teej")

        if language == "hi":
            answer = (
                f"### 🏮 सांस्कृतिक विवरण: **{fest_display}**\n\n"
                f"**महत्व**: {fest_display} स्थानीय रूप से मनाया जाने वाला एक अत्यंत महत्वपूर्ण और पावन त्योहार है। "
                f"यह त्योहार आपसी सद्भाव, सामुदायिक एकता, और समृद्ध सांस्कृतिक विरासत का प्रतीक है।\n\n"
                f"**मुख्य परंपराएं और अनुष्ठान**:\n"
                f"- घरों को सुंदर रंगोली, मिट्टी के दीयों और रोशनी से सजाना।\n"
                f"- कुल देवी-देवताओं की पूजा करना और विशेष पकवान तैयार करना।\n"
                f"- परिवार, रिश्तेदारों और पड़ोसियों को मिठाइयाँ बाँटना और शुभकामनाएं देना।"
            )
        elif language == "te":
            answer = (
                f"### 🏮 సాంస్కృతిక విశేషాలు: **{fest_display}**\n\n"
                f"**ప్రాముఖ్యత**: {fest_display} అనేది స్థానికంగా జరుపుకునే అత్యంత వైవిధ్యమైన మరియు ఉత్సాహభరితమైన పండుగ. "
                f"ఇది సమాజం యొక్క ఐక్యత, సంతోషం మరియు సాంస్కృతిక వారసత్వానికి ప్రతీకగా నిలుస్తుంది.\n\n"
                f"**ప్రధాన ఆచారాలు & సంప్రదాయాలు**:\n"
                f"- ఇళ్లను రంగురంగుల ముగ్గులు మరియు సాంప్రదాయ దీపాలతో అలంకరించడం.\n"
                f"- దేవతలకు ప్రత్యేక నైవేద్యాలను సమర్పించి ధూప దీప నైవేద్యాలతో పూజలు చేయడం.\n"
                f"- కుటుంబ సభ్యులు మరియు పొరుగువారితో పిండివంటలు మరియు శుభాకాంక్షలను పంచుకోవడం."
            )
        else:
            answer = (
                f"### 🏮 Cultural Overview: **{fest_display}**\n\n"
                f"**Significance**: {fest_display} is a highly vibrant and significant festival celebrated locally. "
                f"It symbolises community unity, festive joy, and cultural pride.\n\n"
                f"**Key Customs & Rituals**:\n"
                f"- Adorning houses with colourful decorations and traditional lights.\n"
                f"- Offering specialized festive foods and prayers to deities.\n"
                f"- Exchanging sweets and warm greetings with family and neighbours."
            )
    # 3. Fallback
    else:
        if language == "hi":
            answer = f"**{city_name_local}** सांस्कृतिक साथी में आपका स्वागत है! {provider} प्रदाता का उपयोग करके हिन्दी में जानकारी प्राप्त करें।"
        elif language == "te":
            answer = f"**{city_name_local}** సాంస్కృతిక తోడుకు స్వాగతం! {provider} ఉపయోగించి తెలుగులో సమాచారం పొందండి."
        else:
            answer = f"Welcome to the **{city_name_local}** Cultural Companion! Asking queries in English using {provider}."

    # 4. Phrase assistant response based on selected city (using Telugu/Hindi equivalents)
    if is_hyd:
        phrases = [
            {"phrase": "Hello / Good morning", "translation": "నమస్కారం (Namaskaram)", "pronunciation": "Nah-mah-skah-rum"},
            {"phrase": "How much is this?", "translation": "ఇది ఎంత? (Idi entha?)", "pronunciation": "Ee-dee en-tah?"},
            {"phrase": "Where is Charminar?", "translation": "చార్మినార్ ఎక్కడ ఉంది? (Charminar ekkada undi?)", "pronunciation": "Char-mee-nar ek-kah-dah oon-dee?"},
            {"phrase": "The food is delicious!", "translation": "ఆహారం చాలా రుచిగా ఉంది! (Aaharam chala ruchiga undi!)", "pronunciation": "Aa-haa-rum chaa-lah roo-chee-gah oon-dee"},
            {"phrase": "Thank you", "translation": "ధన్యవాదాలు (Dhanyavadalu)", "pronunciation": "Dhun-yah-vah-dah-loo"}
        ]
    elif is_var:
        phrases = [
            {"phrase": "Hello / Greetings", "translation": "नमस्ते (Namaste) / प्रणाम (Pranam)", "pronunciation": "Nah-muh-stay / Pruh-naam"},
            {"phrase": "Where is the Dashashwamedh Ghat?", "translation": "दशाश्वमेध घाट कहाँ है? (Dashashwamedh Ghat kahan hai?)", "pronunciation": "Duh-shaash-wuh-maydh Ghaat kuh-haan hai?"},
            {"phrase": "How much is this boat ride?", "translation": "नाव की सवारी का कितना हुआ? (Naav ki sawari ka kitna hua?)", "pronunciation": "Naav kee suh-waa-ree kaa kit-naa hoo-aa?"},
            {"phrase": "I want a cup of tea", "translation": "मुझे एक कप चाय चाहिए (Mujhe ek cup chai chahiye)", "pronunciation": "Moo-jhay ek cup chaai chaa-hee-ye"},
            {"phrase": "Thank you", "translation": "धन्यवाद (Dhanyavaad)", "pronunciation": "Dhun-yuh-vaad"}
        ]
    elif is_jai:
        phrases = [
            {"phrase": "Hello / Welcome", "translation": "खम्मा घणी (Khamma Ghani)", "pronunciation": "Khum-mah Ghuh-nee"},
            {"phrase": "How are you?", "translation": "आप क्यां हो? (Aap kyaan ho?)", "pronunciation": "Aap kyaan ho?"},
            {"phrase": "Where is Hawa Mahal?", "translation": "हवा महल कहाँ है? (Hawa Mahal kahan hai?)", "pronunciation": "Huh-waa Muh-hul kuh-haan hai?"},
            {"phrase": "Very beautiful", "translation": "घणो चोखो (Ghano Chokho)", "pronunciation": "Ghuh-no Cho-kho"},
            {"phrase": "Thank you", "translation": "धन्यवाद (Dhanyavaad)", "pronunciation": "Dhun-yuh-vaad"}
        ]
    else:
        phrases = [
            {"phrase": "Hello", "translation": "नमस्ते (Namaste) / నమస్కారం (Namaskaram)", "pronunciation": "Nah-muh-stay / Nah-mah-skah-rum"},
            {"phrase": "Thank you", "translation": "धन्यवाद (Dhanyavaad) / ధన్యవాదాలు (Dhanyavadalu)", "pronunciation": "Dhun-yuh-vaad / Dhun-yah-vah-dah-loo"}
        ]

    # 5. Budget breakdown (translate categories dynamically)
    if language == "hi":
        budget = {
            "आवास (Accommodation) 🏨": 40,
            "भोजन (Food & Dining) 🍽️": 25,
            "स्थानीय परिवहन (Local Transport) 🛺": 15,
            "दर्शनीय स्थल (Sightseeing) 🎟️": 12,
            "विविध (Miscellaneous) 🛍️": 8
        }
    elif language == "te":
        budget = {
            "వసతి (Accommodation) 🏨": 40,
            "భోజనం (Food & Dining) 🍽️": 25,
            "స్థానిక రవాణా (Local Transport) 🛺": 15,
            "సందర్శన రుసుములు (Sightseeing) 🎟️": 12,
            "ఇతర ఖర్చులు (Miscellaneous) 🛍️": 8
        }
    else:
        budget = {
            "Accommodation 🏨": 40,
            "Food & Dining 🍽️": 25,
            "Local Transport 🛺": 15,
            "Sightseeing 🎟️": 12,
            "Miscellaneous 🛍️": 8
        }

    return {
        "answer": answer,
        "phrases": phrases,
        "budget": budget
    }

import os
import logging

# Set up logger
logger = logging.getLogger("api_stub")

# Import the backend AI engine dynamically
try:
    from backend.ai_engine import get_response as get_backend_response
    HAS_BACKEND = True
except ImportError:
    HAS_BACKEND = False

# Detailed dynamic itineraries for the mock fallback
ITINERARIES = {
    "hyderabad": {
        "temples": {
            "en": [
                "**Birla Mandir**: Visit the beautiful temple built on a hilltop of white marble with stunning views of Hussain Sagar.",
                "**Chilkur Balaji Temple**: Visit the famous 'Visa Balaji' temple, participating in the peaceful 108 pradakshinas (circumambulations).",
                "**Jagannath Temple**: Explore the grand temple featuring marvelous Orissa-style architecture and serene gardens.",
                "**Sanghi Temple**: Visit the hilltop temple complex featuring traditional South Indian architecture and scenic views.",
                "**Karmanghat Hanuman Temple**: Explore one of the oldest temples in the city, known for its deep spiritual peace and legends.",
                "**Ashtalakshmi Temple**: Visit the beautiful temple on the banks of Mir Alam tank, dedicated to the eight forms of Goddess Lakshmi.",
                "**Peddamma Gudi**: Pay respects at the popular temple in Jubilee Hills, dedicated to the supreme mother goddess.",
                "**Kesari Hanuman Temple**: Visit the historic temple on the banks of Musi River, founded by Samarth Ramdas."
            ],
            "hi": [
                "**बिरला मंदिर**: पहाड़ी पर स्थित सुंदर मंदिर के दर्शन करें, जो सफेद संगमरमर से बना है और हुसैन सागर झील का अद्भुत दृश्य प्रदान करता है।",
                "**चिल्कुर बालाजी मंदिर**: प्रसिद्ध 'वीज़ा बालाजी' मंदिर जाएं और 108 परिक्रमा के साथ शांत आध्यात्मिक अनुभव करें।",
                "**जगन्नाथ मंदिर**: शानदार मंदिर का अन्वेषण करें, जो अपने उड़ीसा-शैली की वास्तुकला और शांत वातावरण के लिए जाना जाता है।",
                "**संघी मंदिर**: पहाड़ी पर स्थित मंदिर परिसर के दर्शन करें, जिसमें पारंपरिक दक्षिण भारतीय वास्तुकला और सुंदर दृश्य शामिल हैं।",
                "**करमनघाट हनुमान मंदिर**: शहर के सबसे पुराने मंदिरों में से एक का अन्वेषण करें, जो अपनी गहरी आध्यात्मिक शांति और किंवदंतियों के लिए जाना जाता है।",
                "**अष्टलक्ष्मी मंदिर**: मीर आलम तालाब के तट पर स्थित सुंदर मंदिर के दर्शन करें, जो देवी लक्ष्मी के आठ रूपों को समर्पित है।",
                "**पेडदम्मा गुड़ी**: जुबली हिल्स में स्थित प्रसिद्ध मंदिर में दर्शन करें, जो सर्वोच्च मातृ देवी को समर्पित है।",
                "**केसरी हनुमान मंदिर**: मूसी नदी के तट पर स्थित ऐतिहासिक मंदिर के दर्शन करें, जिसकी स्थापना समर्थ रामदास ने की थी।"
            ],
            "te": [
                "**బిర్లా మందిరం**: హుస్సేన్ సాగర్ సుందరమైన దృశ్యాలను అందించే, కొండపై తెల్లటి మార్బుల్‌తో నిర్మించిన బిర్లా మందిరాన్ని సందర్శించండి.",
                "**చిల్కూరు బాలాజీ ఆలయం**: ప్రసిద్ధ 'వీసా బాలాజీ' ఆలయాన్ని సందర్శించి, ప్రశాంతమైన వాతావరణంలో 108 ప్రదక్షిణలు చేయండి.",
                "**జగన్నాథ ఆలయం**: అద్భుతమైన ఒరిస్సా శైలి నిర్మాణ కళతో అలరారే జగన్నాథ ఆలయాన్ని మరియు దాని ప్రశాంత వాతావరణాన్ని అన్వేషించండి.",
                "**సంఘీ దేవాలయం**: సాంప్రదాయ దక్షిణ భారత నిర్మాణ శైలి మరియు సుందరమైన దృశ్యాలతో కూడిన కొండపై గల ఆలయ సముదాయాన్ని సందర్శించండి.",
                "**కర్మన్‌ఘాట్ హనుమాన్ ఆలయం**: నగరంలోని అత్యంత పురాతన ఆలయాలలో ఒకటైన ఈ ఆలయాన్ని సందర్శించి ఆధ్యాత్మిక ప్రశాంతతను పొందండి.",
                "**అష్టలక్ష్మి దేవాలయం**: లక్ష్మీ దేవి యొక్క ఎనిమిది రూపాలకు అంకితం చేయబడిన, మీర్ ఆలం చెరువు సమీపంలోని అందమైన ఆలయాన్ని సందర్శించండి.",
                "**పెద్దమ్మ గుడి**: జూబ్లీహిల్స్ లో ఉన్న ప్రసిద్ధ పెద్దమ్మ తల్లి ఆలయాన్ని సందర్శించి అమ్మవారి కృపకు పాత్రులవండి.",
                "**కేసరి హనుమాన్ ఆలయం**: మూసీ నది ఒడ్డున సమర్థ రామదాసు చేత స్థాపించబడిన చారిత్రక హనుమాన్ ఆలయాన్ని సందర్శించండి."
            ]
        },
        "food": {
            "en": [
                "**Local Dining**: Try hot Irani Chai & Osmania Biscuits at Nimrah Cafe. For dinner, experience the authentic slow-cooked Hyderabadi Dum Biryani with Mirchi ka Salan at Shadab or Cafe Bahar.",
                "**Street Food Walk**: Relish delicious local street food near Charminar (shawarma, pathar ka gosht). Savor the rich double-ka-meetha dessert.",
                "**Nizami Feast**: Enjoy a Nizami royal dinner featuring haleem, spicy kebabs, and sheer khurma at a traditional restaurant.",
                "**Mozamjahi Market**: Head to Famous Ice Cream for unique fruit-flavored hand-churned ice creams.",
                "**Hameedi Confectionery**: Try the legendary Jauzi Halwa, a centuries-old royal sweet flavored with nutmeg.",
                "**Sindhi Colony**: Relish North Indian street foods, savory chats, and famous paneer tikka rolls.",
                "**Ram ki Bandi**: Experience the famous late-night butter-dosa crawl and sample cheese tawa idli.",
                "**Gokul Chat**: Try the legendary hot samosa ragda, bhel puri, and cold dahi puri."
            ],
            "hi": [
                "**स्थानीय भोजन**: निमरा कैफे में गरमा-गरम ईरानी चाय और उस्मानिया बिस्कुट का स्वाद लें। रात के भोजन के लिए शादाब या कैफे बहार में प्रसिद्ध हैदराबादी दम बिरयानी का आनंद लें।",
                "**स्ट्रीट फूड वॉक**: चारमीनार के पास स्वादिष्ट स्थानीय स्ट्रीट फूड (शवारमा, पत्थर का गोश्त) का आनंद लें और प्रसिद्ध डबल का मीठा खाएं।",
                "**निजामी दावत**: एक पारंपरिक रेस्तरां में हलीम, मसालेदार कबाब और शीर खुरमा के साथ एक शाही निजामी रात्रिभोज का आनंद लें।",
                "**मोज़मजाही मार्केट**: अनोखे फलों के स्वाद वाली हाथ से मथी हुई आइसक्रीम के लिए फेमस आइसक्रीम स्टॉल पर जाएँ।",
                "**हमीदी कन्फेक्शनरी**: जायफल के स्वाद वाली सदियों पुरानी शाही मिठाई प्रसिद्ध जौजी हलवा का स्वाद लें।",
                "**सिंधी कॉलोनी**: उत्तर भारतीय स्ट्रीट फूड, स्वादिष्ट चाट और प्रसिद्ध पनीर टिक्का रोल का आनंद लें।",
                "**राम की बांडी**: देर रात प्रसिद्ध मक्खन-डोसा और तवा इडली का स्वाद लेने का अनुभव करें।",
                "**गोकुल चाट**: प्रसिद्ध समोसा रगड़ा, भेल पुरी और ठंडी दही पुरी का आनंद लें।"
            ],
            "te": [
                "**స్థానిక వంటకాలు**: నిమ్రా కేఫ్‌లో వేడి వేడి ఇరానీ చాయ్ మరియు ఉస్మానియా బిస్కెట్లతో ప్రారంభించండి. రాత్రి విందుకు షాదాబ్ లేదా కేఫ్ బహార్‌లో ప్రామాణికమైన హైదరాబాదీ దమ్ బిర్యానీని ఆస్వాదించండి.",
                "**వీధి ఆహార విహారం**: చార్మినార్ సమీపంలో లభించే రుచికరమైన స్థానిక వంటకాలు (షవర్మా, పత్తర్ కా గోష్ట్) మరియు డబుల్ కా మీఠా స్వీట్ రుచి చూడండి.",
                "**నిజామీ రాజవిందు**: సాంప్రదాయ రెస్టారెంట్‌లో రుచికరమైన హలీమ్, కబాబ్స్ మరియు షీర్ కుర్మాలతో కూడిన నిజామీ రాజవిందును ఆస్వాదించండి.",
                "**మోజాంజాహి మార్కెట్**: ప్రత్యేకమైన పండ్ల రుచులతో తయారు చేసే చేతి ఐస్ క్రీం కోసం ఫేమస్ ఐస్ క్రీం సెంటర్ కి వెళ్ళండి.",
                "**హమీది కాన్ఫెక్షనరీ**: జాపత్రితో రుచిగా తయారు చేయబడిన శతాబ్దాల నాటి రాజరిక స్వీట్ 'జౌజీ హల్వా'ను రుచి చూడండి.",
                "**సింధి కాలనీ**: ఉత్తర భారత వీధి ఆహారాలు, చాట్స్ మరియు ప్రసిద్ధ పనీర్ టిక్కా రోల్స్ ఆస్వాదించండి.",
                "**రామ్ కీ బండి**: అర్ధరాత్రి లభించే ప్రసిద్ధ బటర్ దోసలు మరియు తవా ఇడ్లీల రుచిని అనుభవించండి.",
                "**గోకుల్ చాట్**: ఇక్కడి ప్రసిద్ధ సమోసా రగ్డా, భేల్ పూరి మరియు చల్లని దహీ పూరీలను ప్రయత్నించండి."
            ]
        },
        "shopping": {
            "en": [
                "**Laad Bazaar**: Explore the historic bazaar near Charminar, world-famous for traditional lacquer bangles, pearls, and ethnic fabrics.",
                "**Shilparamam**: Visit the arts and crafts village in Madhapur to purchase authentic handicrafts directly from local artisans.",
                "**Pearl Shopping**: Browse specialized pearl showrooms for high-quality Hyderabad pearls and local handloom souvenirs.",
                "**Moazzam Jahi Market**: Shop for high-quality local perfumes (ittar), dried fruits, and fresh local produce.",
                "**Begum Bazar**: Visit the busiest wholesale commercial market for brassware, household goods, and traditional items.",
                "**General Bazar**: Shop for beautiful traditional handloom sarees, dress materials, and wedding clothes.",
                "**Numaish Exhibition**: Experience the grand annual exhibition shopping for carpets, pottery, and state crafts (if seasonal).",
                "**Koti Sultan Bazar**: Browse the busy streets for budget fashion, books, and accessories."
            ],
            "hi": [
                "**लाड बाजार**: चारमीनार के पास ऐतिहासिक बाजार का अन्वेषण करें, जो लाख की चूड़ियों, मोतियों और पारंपरिक कपड़ों के लिए विश्व प्रसिद्ध है।",
                "**शिल्परामम**: माधापुर में शिल्पग्राम जाएं और स्थानीय कारीगरों से सीधे हस्तशिल्प वस्तुएं खरीदें।",
                "**मोती खरीदारी**: गुणवत्तापूर्ण हैदराबादी मोतियों और स्मृति चिन्हों के लिए विशेष मोती शोरूम का दौरा करें।",
                "**मोअज्जम जाही मार्केट**: उच्च गुणवत्ता वाले स्थानीय इत्र, सूखे मेवे और ताजी स्थानीय उपज की खरीदारी करें।",
                "**बेगम बाजार**: पीतल के बर्तन, घरेलू सामान और पारंपरिक वस्तुओं के लिए सबसे व्यस्त थोक बाजार का दौरा करें।",
                "**जनरल बाजार**: सुंदर पारंपरिक हथकरघा साड़ियों, कपड़ों और शादी के परिधानों की खरीदारी करें।",
                "**नुमाइश प्रदर्शनी**: कालीनों, बर्तनों और राज्य के शिल्पों की खरीदारी के लिए भव्य वार्षिक प्रदर्शनी का अनुभव करें।",
                "**कोटी सुल्तान बाजार**: बजट फैशन, किताबों और एक्सेसरीज़ के लिए व्यस्त सड़कों पर घूमें।"
            ],
            "te": [
                "**లాడ్ బజార్**: చార్మినార్ సమీపంలోని చారిత్రక లాడ్ బజార్‌లో లభించే సాంప్రదాయ గాజులు, ముత్యాలు మరియు చేనేత వస్త్రాలను కొనుగోలు చేయండి.",
                "**శిల్పారామం**: మాధాపూర్‌లోని శిల్పారామం క్రాఫ్ట్స్ విలేజ్ సందర్శించి, స్థానిక కళాకారుల నుండి నేరుగా హస్తకళా వస్తువులను సేకరించండి.",
                "**ముత్యాల షాపింగ్**: నాణ్యమైన హైదరాబాద్ ముత్యాలు మరియు జ్ఞాపికల కోసం ప్రత్యేక ముత్యాల షోరూమ్‌లను సందర్శించండి.",
                "**మొజాం జాహీ మార్కెట్**: నాణ్యమైన స్థానిక అత్తరులు, ఎండు ద్రాక్షలు మరియు తాజా పండ్ల కొనుగోలు చేయండి.",
                "**బేగం బజార్**: ఇత్తడి సామాగ్రి, గృహోపకరణాలు మరియు సాంప్రదాయ వస్తువులకు ప్రసిద్ధి చెందిన అతిపెద్ద హోల్‌సేల్ మార్కెట్‌ను సందర్శించండి.",
                "**జనరల్ బజార్**: అందమైన చేనేత చీరలు, వస్త్రాలు మరియు పెళ్లి బట్టల షాపింగ్ కోసం ఇక్కడికి వెళ్ళండి.",
                "**నుమాయిష్ ఎగ్జిబిషన్**: వార్షిక ఎగ్జిబిషన్ లో రకరకాల తివాచీలు, మట్టి పాత్రలు మరియు హస్తకళల వస్తువులను కొనుగోలు చేయండి.",
                "**కోఠి సుల్తాన్ బజార్**: బడ్జెట్ ధరలలో లభించే దుస్తులు, పుస్తకాలు మరియు వస్తువుల కోసం ఈ బజార్ ను సందర్శించండి."
            ]
        },
        "history": {
            "en": [
                "**Golconda Fort**: Explore Golconda Fort, renowned for its acoustic effects at Fateh Darwaza and Bala Hissar. Watch the evening light & sound show.",
                "**Chowmahalla Palace**: Visit the historic seat of the Nizams, reflecting majestic architecture, vintage cars, and grand halls.",
                "**Salar Jung & Charminar**: Visit Salar Jung Museum, housing one of the largest private collections, and climb the iconic Charminar.",
                "**Qutb Shahi Tombs**: Visit the grand landscaped tombs of the founding rulers of Hyderabad, displaying a blend of Persian and Hindu styles.",
                "**Falaknuma Palace**: Take a heritage walk around the palace of the Nizams, famous for its Italian marble and massive dining hall.",
                "**Purani Haveli**: Visit the residence of the Nizams, featuring the world's longest wardrobe and historical museum exhibits.",
                "**Paigah Tombs**: Discover the intricately carved marble tombs of the noble Paigah family, displaying stunning craftsmanship.",
                "**Mecca Masjid**: Admire the historical mosque constructed using soil brought from Mecca, next to Charminar."
            ],
            "hi": [
                "**गोलकोंडा किला**: गोलकोंडा किला देखें (फतेह दरवाजा और बाला हिसार पर ध्वनिक प्रभावों का अनुभव करें) और शाम को लाइट एंड साउंड शो का आनंद लें।",
                "**चौमहल्ला पैलेस**: निजामों के ऐतिहासिक निवास चौमहल्ला पैलेस का दौरा करें, जो अपनी भव्य वास्तुकला, विंटेज कारों और बड़े हॉलों के लिए प्रसिद्ध है।",
                "**सालार जंग और चारमीनार**: सालार जंग संग्रहालय का दौरा करें, जिसमें दुनिया के सबसे बड़े निजी कला संग्रहों में से एक है, और चारमीनार पर चढ़ें।",
                "**कुतुब शाही मकबरे**: हैदराबाद के संस्थापक शासकों के भव्य मकबरों के दर्शन करें, जो फारसी और हिंदू शैलियों का मिश्रण प्रदर्शित करते हैं।",
                "**फलकनुमा पैलेस**: निजामों के महल के आसपास एक विरासत वॉक करें, जो अपने इतालवी संगमरमर और विशाल भोजन कक्ष के लिए प्रसिद्ध है।",
                "**पुरानी हवेली**: निजामों के निवास का दौरा करें, जिसमें दुनिया की सबसे लंबी अलमारी और ऐतिहासिक संग्रहालय प्रदर्शनियां हैं।",
                "**पैगाह मकबरे**: शानदार शिल्प कौशल प्रदर्शित करने वाले महान पैगाह परिवार के जटिल नक्काशीदार संगमरमर के मकबरों की खोज करें।",
                "**मक्का मस्जिद**: चारमीनार के बगल में स्थित मक्का से लाई गई मिट्टी से निर्मित ऐतिहासिक मस्जिद की भव्यता की प्रशंसा करें।"
            ],
            "te": [
                "**గోల్కొండ కోట**: గోల్కొండ కోటను సందర్శించండి (ఫతే దర్వాజా మరియు బాలా హిసార్ వద్ద ఉండే ప్రత్యేక శబ్ద తరంగాల అనుభూతిని పొందండి) మరియు సాయంత్రం లైట్ అండ్ సౌండ్ షోను తిలకించండి.",
                "**చౌమహల్లా ప్యాలెస్**: నిజాం రాజుల చారిత్రక నివాసమైన చౌమహల్లా ప్యాలెస్ అద్భుతమైన రాజరిక వైభవాన్ని, వింటేజ్ కార్లను మరియు విశాలమైన హాల్స్ సందర్శించండి.",
                "**సాలార్ జంగ్ & చార్మినార్**: ప్రపంచంలోనే అతిపెద్ద ప్రైవేట్ ఆర్ట్ కలెక్షన్లలో ఒకటైన సాలార్ జంగ్ మ్యూజియంను సందర్శించి, ఐకానిక్ చార్మినార్‌ను ఎక్కండి.",
                "**కుతుబ్ షాహీ సమాధులు**: పర్షియన్ మరియు హిందూ నిర్మాణ శైలి సమ్మేళనంతో నిర్మించబడిన కుతుబ్ షాహీ పాలకుల సమాధులను సందర్శించండి.",
                "**ఫలక్‌నుమా ప్యాలెస్**: ఇటాలియన్ మార్బుల్ మరియు భారీ డైనింగ్ హాల్ కు ప్రసిద్ధి చెందిన నిజాంల ప్యాలెస్ చుట్టూ హెరిటేజ్ వాక్ చేయండి.",
                "**పురాణి హవేలీ**: ప్రపంచంలోనే అతిపెద్ద వార్డ్‌రోబ్ మరియు చారిత్రక మ్యూజియం గల నిజాంల నివాసమైన పురాణి హవేలీని సందర్శించండి.",
                "**పైగా సమాధులు**: అద్భుతమైన శిల్పకళతో అలంకరించబడిన పైగా వంశీయుల అందమైన పాలరాతి సమాధులను సందర్శించండి.",
                "**మక్కా మసీదు**: మక్కా నుండి తెచ్చిన మట్టితో చార్మినార్ పక్కనే నిర్మించబడిన చారిత్రక మక్కా మసీదును సందర్శించండి."
            ]
        },
        "default": {
            "en": [
                "**Golconda Fort**: Explore the primary historical fortress in Hyderabad and enjoy local Hyderabadi snacks.",
                "**Charminar & Laad Bazaar**: Delight in local traditional street food near Charminar, visit the bazaar, and try Irani Chai.",
                "**Chowmahalla Palace & Shopping**: Pick up pearl souvenirs from local showrooms and farewell dinner at a Nizam cuisine restaurant.",
                "**Hussain Sagar & Birla Mandir**: Visit the white marble temple on the hilltop and enjoy a boat ride on the lake.",
                "**Salar Jung Museum**: Explore the massive art collection and the historical treasures of the region.",
                "**Ramoji Film City**: Spend a full day exploring the world's largest integrated film studio complex.",
                "**Qutb Shahi Tombs**: Visit the ancient domed tombs of the seven Qutb Shahi rulers, reflecting rich heritage.",
                "**Nehru Zoological Park**: Enjoy a morning safari and visit the animal conservation exhibits."
            ],
            "hi": [
                "**गोलकोंडा किला**: हैदराबाद के प्रमुख ऐतिहासिक किले का भ्रमण करें और स्थानीय हैदराबादी व्यंजनों का स्वाद लें।",
                "**चारमीनार और लाड बाजार**: चारमीनार के पास पारंपरिक व्यंजनों का आनंद लें, बाजार घूमें और ईरानी चाय का आनंद लें।",
                "**चौमहल्ला पैलेस और खरीदारी**: प्रसिद्ध बाजारों से मोती और उपहार खरीदें और विशेष विदारी रात्रिभोज के साथ यात्रा समाप्त करें।",
                "**हुसैन सागर और बिरला मंदिर**: पहाड़ी पर स्थित सफेद संगमरमर के मंदिर के दर्शन करें और झील में नौका विहार का आनंद लें।",
                "**सालार जंग संग्रहालय**: विशाल कला संग्रह और क्षेत्र के ऐतिहासिक खजानों का अन्वेषण करें।",
                "**रामोजी फिल्म सिटी**: दुनिया के सबसे बड़े एकीकृत फिल्म स्टूडियो परिसर की खोज में एक पूरा दिन बिताएं।",
                "**कुतुब शाही मकबरे**: समृद्ध विरासत को दर्शाने वाले सात कुतुब शाही शासकों के प्राचीन गुंबददार मकबरों के दर्शन करें।",
                "**नेहरू प्राणी उद्यान**: सुबह की सफारी का आनंद लें और पशु संरक्षण प्रदर्शनियों का दौरा करें।"
            ],
            "te": [
                "**గోల్కొండ కోట**: హైదరాబాద్ లోని ప్రధాన చారిత్రక కోటను సందర్శించి స్థానిక రుచులను ఆస్వాదించండి.",
                "**చార్మినార్ & లాడ్ బజార్**: చార్మినార్ సమీపంలో వీధి ఆహారాలను రుచి చూసి, బజార్లలో షాపింగ్ చేసి ఇరానీ చాయ్ తాగండి.",
                "**చౌమహల్లా ప్యాలెస్ & ముత్యాలు**: బజార్ల నుండి స్థానిక ముత్యాల జ్ఞాపికలను కొనుగోలు చేసి ప్రత్యేక విందుతో ప్రయాణాన్ని ముగించండి.",
                "**హుస్సేన్ సాగర్ & బిర్లా మందిరం**: కొండపై తెల్లటి మార్బుల్‌తో కట్టిన బిర్లా మందిరాన్ని దర్శించి, చెరువులో బోటింగ్ చేయండి.",
                "**సాలార్ జంగ్ మ్యూజియం**: అద్భుతమైన చారిత్రక వస్తువులు మరియు భారీ కళాఖండాల సేకరణను అన్వేషించండి.",
                "**రామోజీ ఫిల్మ్ సిటీ**: ప్రపంచంలోనే అతిపెద్ద ఇంటిగ్రేటెడ్ ఫిల్మ్ స్టూడియో కాంప్లెక్స్‌ను రోజంతా అన్వేషించండి.",
                "**కుతుబ్ షాహీ సమాధులు**: ఏడుగురు కుతుబ్ షాహీ పాలకుల పురాతన సమాధులను సందర్శించి చారిత్రక విశేషాలను తెలుసుకోండి.",
                "**నెహ్రూ జూలాజికల్ పార్క్**: ఉదయాన్నే సఫారీని ఆస్వాదించండి మరియు జంతు ప్రదర్శనశాలను సందర్శించండి."
            ]
        },
        "nature": {
            "en": [
                "**KBR National Park**: Visit the lush green national park in the heart of the city, perfect for quiet morning walks and spotting local birds.",
                "**Hussain Sagar & NTR Gardens**: Take a scenic walk along the lake, view the giant Buddha statue, and relax in the manicured gardens.",
                "**Ananthagiri Hills**: Day excursion to the scenic forest hills near the city, offering beautiful valleys and trekking trails.",
                "**Durgam Cheruvu**: Walk along the secret lake promenade and admire the modern cable bridge lit up at night.",
                "**Nehru Zoological Park**: Explore the massive zoo featuring a safari park and a wide variety of wildlife.",
                "**Botanical Garden**: Walk through the serene garden paths in Kondapur, showcasing rich flora and medicinal plants.",
                "**Osman Sagar**: Enjoy a peaceful sunset at the Gandipet lake reservoir, surrounded by nature.",
                "**Mrugavani National Park**: Experience a safari to spot deer and local bird species in their natural habitat."
            ],
            "hi": [
                "**केबीआर राष्ट्रीय उद्यान**: शहर के बीचोबीच स्थित इस हरे-भरे राष्ट्रीय उद्यान का दौरा करें, जो सुबह की सैर और पक्षियों को देखने के लिए उत्तम है।",
                "**हुसैन सागर और एनटीआर गार्डन**: झील के किनारे टहलें, विशाल बुद्ध प्रतिमा को देखें, और सुंदर बगीचों में आराम करें।",
                "**अनंतगिरी पहाड़ियाँ**: सुंदर वन पहाड़ियों की सैर करें, जो सुंदर घाटियों और ट्रेकिंग ट्रेल्स की पेशकश करती हैं।",
                "**दुर्गम चेरुवु**: गुप्त झील के सैरगाह पर टहलें और रात में रोशनी से सजे आधुनिक केबल ब्रिज की प्रशंसा करें।",
                "**नेहरू प्राणी उद्यान**: सफारी पार्क और वन्यजीवों की एक विस्तृत विविधता वाले विशाल चिड़ियाघर का अन्वेषण करें।",
                "**वानस्पतिक उद्यान**: कोंडापुर में शांत उद्यान पथों से गुजरें, जो समृद्ध वनस्पतियों और औषधीय पौधों को प्रदर्शित करते हैं।",
                "**उस्मान सागर**: प्रकृति से घिरे गांधीपेट झील जलाशय में एक शांतिपूर्ण सूर्यास्त का आनंद लें।",
                "**मृगावनी राष्ट्रीय उद्यान**: प्राकृतिक आवास में हिरणों और स्थानीय पक्षी प्रजातियों को देखने के लिए सफारी का अनुभव करें।"
            ],
            "te": [
                "**కెబిఆర్ నేషనల్ పార్క్**: నగర నడిబొడ్డున ఉన్న పచ్చని పార్కును సందర్శించండి, ప్రశాంతమైన ఉదయపు నడకకు మరియు స్థానిక పక్షులను చూడటానికి ఇది అనువైనది.",
                "**హుస్సేన్ సాగర్ & ఎన్టీఆర్ గార్డెన్స్**: సరస్సు వెంబడి నడుస్తూ, భారీ బుద్ధ విగ్రహాన్ని వీక్షించండి మరియు అందమైన తోటలలో విశ్రాంతి తీసుకోండి.",
                "**అనంతగిరి కొండలు**: లోయలు మరియు ట్రెక్కింగ్ మార్గాలతో కూడిన సుందరమైన అడవి కొండలకు విహారయాత్ర చేయండి.",
                "**దుర్గం చెరువు**: సీక్రెట్ లేక్ ప్రొమెనేడ్ వెంబడి నడుస్తూ రాత్రి పూట కాంతులతో వెలిగిపోయే కేబుల్ బ్రిడ్జిని తిలకించండి.",
                "**నెహ్రూ జూలాజికల్ పార్క్**: సఫారీ పార్క్ మరియు అనేక రకాల వన్యప్రాణులతో కూడిన భారీ జూను అన్వేషించండి.",
                "**బొటానికల్ గార్డెన్**: కొండాపూర్‌లోని ప్రశాంతమైన తోట మార్గాల గుండా నడుస్తూ అందమైన మొక్కలను సందర్శించండి.",
                "**ఉస్మాన్ సాగర్**: గండిపేట చెరువు వద్ద ప్రకృతి ఒడిలో ప్రశాంతమైన సూర్యాస్తమయ దృశ్యాన్ని ఆస్వాదించండి.",
                "**మృగవని నేషనల్ పార్క్**: వాటి సహజ ఆవాసాలలో జింకలు మరియు స్థానిక పక్షులను చూడటానికి సఫారీని అనుభవించండి."
            ]
        }
    },
    "varanasi": {
        "temples": {
            "en": [
                "**Kashi Vishwanath**: Visit the sacred Golden Temple dedicated to Lord Shiva, the spiritual center of the city.",
                "**Ganga Aarti**: Witness the breathtaking, spiritual evening oil-lamp ritual at Dashashwamedh Ghat.",
                "**Sankat Mochan Temple**: Visit the historic temple dedicated to Lord Hanuman, filled with devotional chants.",
                "**Durga Kund Temple**: Explore the grand 18th-century temple built in red stone, reflecting architectural beauty.",
                "**Tulsi Manas Mandir**: Visit the marble temple where saint-poet Tulsidas wrote the Ramcharitmanas epic.",
                "**New Vishwanath Temple**: Explore the tall white marble temple inside the Banaras Hindu University campus.",
                "**Lalita Gauri Temple**: Pay respects at the historic ghat-side temple dedicated to Goddess Lalita.",
                "**Nepali Temple**: Visit the unique wooden temple displaying traditional pagoda-style architecture."
            ],
            "hi": [
                "**काशी विश्वनाथ**: भगवान शिव को समर्पित पवित्र स्वर्ण मंदिर के दर्शन करें, जो शहर का आध्यात्मिक केंद्र है।",
                "**गंगा आरती**: दशाश्वमेध घाट पर शाम को होने वाले शानदार, आध्यात्मिक तेल-दीपक अनुष्ठान का अनुभव करें।",
                "**संकट मोचन मंदिर**: भगवान हनुमान को समर्पित ऐतिहासिक मंदिर के दर्शन करें, जो भक्ति भजनों से गूंजता रहता है।",
                "**दुर्गा कुंड मंदिर**: लाल पत्थर से बने भव्य 18वीं शताब्दी के मंदिर का अन्वेषण करें, जो स्थापत्य कला का सुंदर उदाहरण है।",
                "**तुलसी मानस मंदिर**: संगमरमर के उस मंदिर के दर्शन करें जहां संत-कवि तुलसीदास ने रामचरितमानस महाकाव्य की रचना की थी।",
                "**नवीन विश्वनाथ मंदिर**: बनारस हिंदू विश्वविद्यालय परिसर के भीतर स्थित ऊंचे सफेद संगमरमर के मंदिर का भ्रमण करें।",
                "**ललिता गौरी मंदिर**: घाट किनारे स्थित देवी ललिता को समर्पित ऐतिहासिक मंदिर में मत्था टेकें।",
                "**नेपाली मंदिर**: पारंपरिक पैगोडा-शैली की वास्तुकला को प्रदर्शित करने वाले अनोखे लकड़ी के मंदिर के दर्शन करें।"
            ],
            "te": [
                "**కాశీ విశ్వనాథ్**: శివునికి అంకితం చేయబడిన పవిత్రమైన స్వర్ణ దేవాలయాన్ని సందర్శించండి, ఇది నగర ఆధ్యాత్మిక కేంద్రం.",
                "**గంగా హారతి**: దశాశ్వమేధ ఘాట్ వద్ద సాయంత్రం జరిగే అద్భుతమైన మరియు ఆధ్యాత్మిక హారతి సేవను వీక్షించండి.",
                "**సంకట మోచన ఆలయం**: భక్తి కీర్తనలతో నిండి ఉండే హనుమంతుని చారిత్రక ఆలయాన్ని సందర్శించండి.",
                "**దుర్గా కుండ్ ఆలయం**: ఎర్రటి రాయితో కట్టిన, అద్భుత శిల్పకళతో అలరారే 18వ శతాబ్దపు ఆలయాన్ని అన్వేషించండి.",
                "**తులసి మానస్ మందిర్**: తులసీదాస్ కవి రామచరితమానస్ గ్రంథాన్ని రచించిన స్థలంలో నిర్మించిన పాలరాతి మందిరాన్ని సందర్శించండి.",
                "**న్యూ విశ్వనాథ్ ఆలయం**: బనారస్ హిందూ యూనివర్సిటీ (BHU) ఆవరణలోని ఎత్తైన తెల్లటి పాలరాతి ఆలయాన్ని సందర్శించండి.",
                "**లలితా గౌరీ దేవాలయం**: ఘాట్ సమీపంలో దేవీ లలితా గౌరీకి అంకితం చేయబడిన పురాతన ఆలయాన్ని దర్శించండి.",
                "**నేపాలీ దేవాలయం**: సాంప్రదాయ పగోడా శైలి నిర్మాణాన్ని ప్రదర్శించే ప్రత్యేకమైన చెక్క ఆలయాన్ని సందర్శించండి."
            ]
        },
        "food": {
            "en": [
                "**Varanasi Breakfast**: Enjoy a traditional breakfast of Kachori Sabzi and hot Jalebi. In the evening, try spicy Tamatar Chaat and cold Lassi in kulhads.",
                "**Baati Chokha**: Taste the rustic and delicious Baati Chokha at a local restaurant, and try the legendary Banarasi Paan.",
                "**Ghat Sweets**: Sample local sweets like Rabri and the seasonal, airy Malaiyo from street stalls near the ghats.",
                "**Blue Lassi**: Visit the famous corner shop to relish thick lassis topped with seasonal fruits and dry fruits.",
                "**Deena Chaat Bhandar**: Try the delicious Gol Gappe, spicy Tamatar Chaat, and sweet Tikki.",
                "**Ram Bhandar**: Savor the legendary Chhena Dahi Vada and rich subzi-kachori breakfast.",
                "**Rajbandhu Sweets**: Indulge in traditional Banarasi sweets like Malai Gilori and dry fruit burfis.",
                "**Local Thandai**: Relish a refreshing glass of traditional almond-flavored spiced milk."
            ],
            "hi": [
                "**वाराणसी का नाश्ता**: वाराणसी का पारंपरिक नाश्ता कचौड़ी-सब्जी और गर्म जलेबी खाएं। शाम को कुल्हड़ में मिलने वाली तीखी टमाटर चाट और मीठी लस्सी का स्वाद लें।",
                "**बाटी चोखा और पान**: एक स्थानीय रेस्तरां में पारंपरिक बाटी-चोखा का स्वाद लें और प्रसिद्ध बनारसी पान खाना न भूलें।",
                "**घाट की मिठाइयाँ**: घाटों के पास के स्टॉलों से स्वादिष्ट राबड़ी और सर्दियों की खास मिठाई मलइयो का आनंद लें।",
                "**ब्लू लस्सी**: मौसमी फलों और सूखे मेवों से भरपूर गाढ़ी लस्सी का आनंद लेने के लिए प्रसिद्ध दुकान पर जाएँ।",
                "**दीना चाट भंडार**: स्वादिष्ट गोल गप्पे, तीखी टमाटर चाट और आलू टिक्की का स्वाद लें।",
                "**राम भंडार**: यहाँ के प्रसिद्ध छैना दही वड़ा और कचौड़ी-सब्जी के नाश्ते का स्वाद लें।",
                "**राजबंधु स्वीट्स**: मलाई गिलोरी और सूखे मेवों की बर्फी जैसी पारंपरिक बनारसी मिठाइयों का आनंद लें।",
                "**स्थानीय ठंडाई**: बादाम के स्वाद वाले पारंपरिक ठंडे दूध के एक ताज़ा गिलास का आनंद लें।"
            ],
            "te": [
                "**వారణాసి అల్పాహారం**: వారణాసి సాంప్రదాయ ఉదయపు ఉపాహారం కచోరీ సబ్జీ మరియు జిలేబీతో ప్రారంభించండి. సాయంత్రం మట్టి కప్పులలో లభించే టమోటా చాట్ మరియు చిక్కటి లస్సీని రుచి చూడండి.",
                "**బాటీ చోఖా & పాన్**: సంప్రదాయ బాటీ చోఖా రుచి చూడండి మరియు ప్రసిద్ధ బనారసి పాన్‌ను తప్పక ప్రయత్ండిచండి.",
                "**ఘాట్ స్వీట్లు**: ఘాట్‌ల సమీపంలోని స్టాల్స్ నుండి స్థానిక స్వీట్లు రబ్రీ మరియు నోట్లో కరిగిపోయే మలైయోను ఆస్వాదించండి.",
                "**బ్లూ లస్సీ**: డ్రై ఫ్రూట్స్ మరియు పండ్ల ముక్కలతో పైన అలంకరించబడిన చిక్కటి లస్సీని తాగడానికి ప్రసిద్ధ దుకాణాన్ని సందర్శించండి.",
                "**దీనా చాట్ భండార్**: రుచికరమైన గోల్ గప్పా, కారంగా ఉండే టమోటా చాట్ మరియు టిక్కీలను రుచి చూడండి.",
                "**రామ్ భండార్**: ఇక్కడి ప్రసిద్ధమైన ఛేనా దహీ వడ మరియు కచోరీల ఉదయపు అల్పాహారాన్ని ఆస్వాదించండి.",
                "**రాజ్ బంధు స్వీట్స్**: మలై గిలోరి మరియు డ్రై ఫ్రూట్ బర్ఫీలు వంటి సాంప్రదాయ బనారసి మిఠాయిలను స్వీకరించండి.",
                "**స్థానిక తాండై**: బాదం పాలు మరియు మసాలాల మిశ్రమంతో కూడిన చల్లని తాండైను ఆస్వాదించండి."
            ]
        },
        "nature": {
            "en": [
                "**Ganga River & Ghats**: Enjoy a scenic walk along the ancient ghats during sunrise, observing the wide and peaceful flow of the Ganges.",
                "**Sarnath Deer Park**: Visit the peaceful and sacred deer park gardens where Lord Buddha taught his first sermon.",
                "**Chandra Prabha Sanctuary**: Take a trip to the nearby scenic wildlife sanctuary featuring beautiful waterfalls and lush forest walks.",
                "**Lakhaniya Dari**: Embark on a nature trek to the beautiful rocky waterfall and serene forest pools nearby.",
                "**Wyndom Falls**: Visit the scenic waterfall and step-like water streams in Mirzapur hills on a day excursion.",
                "**Rajdari & Devdari**: Explore the twin waterfalls located inside the Chandraprabha forest reserve area.",
                "**Assi River Confluence**: Walk down to the scenic point where the Assi River joins the sacred Ganges.",
                "**Ramnagar Forest**: Take a peaceful stroll along the green forest paths on the opposite bank of the Ganges."
            ],
            "hi": [
                "**गंगा नदी और घाट**: सूर्योदय के समय प्राचीन घाटों के किनारे टहलें और गंगा के शांत प्रवाह का आनंद लें।",
                "**सारनाथ हिरण पार्क**: शांत और पवित्र हिरण पार्क का दौरा करें जहाँ भगवान बुद्ध ने अपना पहला उपदेश दिया था।",
                "**चंद्रप्रभा अभयारण्य**: सुंदर झरनों और हरे-भरे जंगलों वाले वन्यजीव अभयारण्य की यात्रा करें।",
                "**लखनिया दरी**: पास में स्थित सुंदर चट्टानी झरने और शांत वन तालाबों के लिए एक प्रकृति ट्रेक पर निकलें।",
                "**विंधम फॉल्स**: एक दिवसीय यात्रा पर मिर्जापुर की पहाड़ियों में स्थित सुंदर झरने और जलधाराओं को देखें।",
                "**राजदरी और देवदरी**: चंद्रप्रभा वन आरक्षित क्षेत्र के भीतर स्थित जुड़वां झरनों का अन्वेषण करें।",
                "**असि नदी संगम**: उस सुंदर बिंदु तक टहलें जहां असि नदी पवित्र गंगा में मिलती है।",
                "**रामनगर वन**: गंगा के दूसरे छोर पर स्थित हरे-भरे वन पथों पर शांतिपूर्ण सैर करें।"
            ],
            "te": [
                "**గంగా నది & ఘాట్‌లు**: సూర్యోదయ సమయంలో పురాతన ఘాట్‌ల వెంబడి నడుస్తూ, ప్రశాంతంగా ప్రవహించే గంగా నదిని వీక్షించండి.",
                "**సార్నాథ్ జింకల పార్క్**: బుద్ధుడు తన మొదటి బోధనను అందించిన ప్రశాంతమైన మరియు పవిత్రమైన జింకల పార్కును సందర్శించండి.",
                "**చంద్రప్రభ అభయారణ్యం**: అందమైన జలపాతాలు మరియు దట్టమైన అడవులతో కూడిన సమీప అభయారణ్యానికి విహారయాత్ర చేయండి.",
                "**లఖనియా దరి**: సమీపంలోని కొండ జలపాతం మరియు ప్రశాంతమైన అడవి గుండా సాగే ట్రెకింగ్ ను ఆస్వాదించండి.",
                "**వింధం జలపాతం**: మిర్జాపూర్ కొండలలోని జలపాతం మరియు నీటి ప్రవాహాలను సందర్శించడానికి విహారయాత్ర చేయండి.",
                "**రాజదరి & దేవదరి**: చంద్రప్రభ అడవి లోపల ఉండే జంట జలపాతాలను సందర్శించి ఆనందించండి.",
                "**అస్సి నది సంగమం**: అస్సి నది పవిత్ర గంగా నదిలో కలిసే సుందరమైన ప్రదేశాన్ని సందర్శించండి.",
                "**రామ్‌నగర్ అడవి**: గంగా నదికి అవతలి వైపున ఉండే ప్రశాంతమైన అడవి మార్గాల గుండా నడవండి."
            ]
        },
        "shopping": {
            "en": [
                "**Banarasi Silk Weavers**: Visit a local weavers' cooperative to see the intricate hand-weaving of world-famous Banarasi Silk Sarees.",
                "**Vishwanath Gali**: Walk through Chowk and Vishwanath Gali markets to buy wooden toys, local clay handicrafts, and religious souvenirs.",
                "**Metal Crafts**: Shop for beautiful copper work, religious idols, and traditional brass items.",
                "**Thatheri Bazar**: Visit the traditional bazaar famous for handmade metal pots, brass utensils, and copper ornaments.",
                "**Godowlia Market**: Shop for local perfumes (ittar), wooden home decor, and woolen shawls.",
                "**Chowk Bazaar**: Explore the central fabric bazaar for hand-woven textiles and Banarasi fabrics.",
                "**Gyanvapi Market**: Browse the colorful stalls selling glass beads, traditional ornaments, and ethnic bags.",
                "**Rajan Silk Store**: Browse high-quality authentic silk textiles directly sourced from weaving families."
            ],
            "hi": [
                "**बनारसी सिल्क बुनकर**: विश्व प्रसिद्ध बनारसी रेशमी साड़ियों (बनारसी सिल्क साड़ी) की बुनाई देखने के लिए स्थानीय बुनकर कॉलोनी का दौरा करें।",
                "**विश्वनाथ गली**: लकड़ी के खिलौने, मिट्टी के हस्तशिल्प और धार्मिक स्मृति चिन्ह खरीदने के लिए चौक और विश्वनाथ गली के बाजारों में घूमें।",
                "**धातु शिल्प**: तांबे के सुंदर बर्तन, धार्मिक मूर्तियाँ और पारंपरिक पीतल की सजावटी वस्तुओं की खरीदारी करें।",
                "**ठठेरी बाजार**: हाथ से बने धातु के बर्तनों, पीतल के बर्तनों और तांबे के आभूषणों के लिए प्रसिद्ध पारंपरिक बाजार का दौरा करें।",
                "**गोदौलिया बाजार**: स्थानीय इत्र (इत्र), लकड़ी की सजावटी वस्तुओं और ऊनी शॉल की खरीदारी करें।",
                "**चौक बाजार**: हाथ से बुने कपड़ों और बनारसी वस्त्रों के लिए केंद्रीय कपड़ा बाजार का अन्वेषण करें।",
                "**ज्ञानवापी बाजार**: कांच के मोतियों, पारंपरिक गहनों और नृवंशविज्ञान बैग बेचने वाले रंगीन स्टालों को देखें।",
                "**राजन सिल्क स्टोर**: बुनकर परिवारों से सीधे प्राप्त उच्च गुणवत्ता वाले रेशम वस्त्रों की खरीदारी करें।"
            ],
            "te": [
                "**బనారసి చేనేత కార్మికులు**: ప్రపంచ ప్రసిద్ధ బనారసి పట్టు చీరల (సిల్క్ శారీస్) మగ్గాల తయారీని గమనించడానికి స్థానిక చేనేత కాలనీని సందర్శించండి.",
                "**విశ్వనాథ్ గల్లీ**: చౌక్ మరియు విశ్వనాథ్ గల్లీ మార్కెట్లను అన్వేషించి చెక్క బొమ్మలు, స్థానిక మట్టి వస్తువులు మరియు ఆధ్యాత్మిక జ్ఞాపికలను కొనుగోలు చేయండి.",
                "**లోహపు హస్తకళలు**: అందమైన రాగి పాత్రలు, దేవతా విగ్రహాలు మరియు సాంప్రదాయ ఇత్తడి వస్తువులను కొనుగోలు చేయండి.",
                "**తఠేరి బజార్**: ఇత్తడి మరియు రాగి పాత్రలకు ప్రసిద్ధి చెందిన పురాతన మెటల్ బజార్ ను సందర్శించండి.",
                "**గోడోలియా మార్కెట్**: స్థానిక అత్తరులు, చెక్క వస్తువులు మరియు శాలువాల కొనుగోలు కోసం ఇక్కడికి వెళ్ళండి.",
                "**చౌక్ బజార్**: చేతితో నేసిన వస్త్రాలు మరియు బనారసి సిల్క్ ప్యాబ్రిక్స్ కోసం ఈ బజార్ ను సందర్శించండి.",
                "**జ్ఞానవాపి మార్కెట్**: రంగురంగుల గాజు పూసలు, వస్తువులు మరియు సాంప్రదాయ బ్యాగుల అమ్మే దుకాణాలను సందర్శించండి.",
                "**రాజన్ సిల్క్ స్టోర్**: చేనేత కుటుంబాల నుండి సేకరించిన నాణ్యమైన పట్టు వస్త్రాలను కొనుగోలు చేయండి."
            ]
        },
        "history": {
            "en": [
                "**Ghat Walking Tour**: Take a walking tour of the ancient ghats of Varanasi, learning about their historical and cultural significance.",
                "**Sarnath Day Trip**: Go on a day trip to Sarnath, where Lord Buddha preached his first sermon after enlightenment. Explore Dhamek Stupa.",
                "**Ramnagar Fort**: Visit the 18th-century Ramnagar Fort containing an exquisite museum of vintage cars, royal palanquins, and medieval weapons.",
                "**Chunar Fort**: Excursion to the massive stone fortress overlooking the Ganges, built by King Vikramaditya.",
                "**Jantar Mantar**: Visit the astronomical observatory built on the roof of Man Mahal overlooking the ghats.",
                "**Bharat Kala Bhavan**: Explore the art and archaeological museum inside the BHU campus, displaying ancient sculptures.",
                "**Alamgir Mosque**: Visit the historical mosque built by Aurangzeb, showcasing a blend of Hindu and Islamic designs.",
                "**Man Mandir Observatory**: Tour the historic ghat-side palace built by Raja Man Singh of Jaipur with stone instruments."
            ],
            "hi": [
                "**घाटों की पैदल यात्रा**: वाराणसी के प्राचीन घाटों की पैदल यात्रा करें और उनके ऐतिहासिक और सांस्कृतिक महत्व के बारे में जानें।",
                "**सारनाथ यात्रा**: सारनाथ की यात्रा करें, जहाँ भगवान बुद्ध ने अपना पहला उपदेश दिया था। धमेख स्तूप और पुरातत्व संग्रहालय का अन्वेषण करें।",
                "**रामनगर किला**: रामनगर किले का दौरा करें, जिसमें पुरानी विंटेज कारों, शाही पालकियों और मध्यकालीन हथियारों का एक बेहतरीन संग्रहालय है।",
                "**चुनार किला**: राजा विक्रमादित्य द्वारा निर्मित गंगा के किनारे विशाल पत्थर के किले की सैर करें।",
                "**जंतर मंतर**: घाटों के किनारे स्थित मान महल की छत पर बनी खगोलीय वेधशाला का दौरा करें।",
                "**भारत कला भवन**: बीएचयू परिसर के अंदर स्थित कला और पुरातात्विक संग्रहालय का अन्वेषण करें, जिसमें प्राचीन मूर्तियाँ प्रदर्शित हैं।",
                "**आलमगीर मस्जिद**: औरंगजेब द्वारा निर्मित ऐतिहासिक मस्जिद का दौरा करें, जो हिंदू और इस्लामी शैलियों का मिश्रण प्रदर्शित करती है।",
                "**मान मंदिर वेधशाला**: जयपुर के राजा मान सिंह द्वारा घाट किनारे निर्मित पत्थर के उपकरणों वाले ऐतिहासिक महल का दौरा करें।"
            ],
            "te": [
                "**ఘాట్ వాకింగ్ టూర్**: వారణాసి పురాతన ఘాట్‌ల గుండా నడుస్తూ, వాటి చారిత్రక మరియు సాంస్కృతిక ప్రాముఖ్యతను తెలుసుకోండి.",
                "**సార్నాథ్ విహారం**: బుద్ధుడు తన మొదటి ఉపన్యాసాన్ని బోధించిన పవిత్ర సార్నాథ్‌ను సందర్శించి, ధమేక్ స్థూపం మరియు పురావస్తు మ్యూజియంను అన్వేషించండి.",
                "**రామ్‌నగర్ కోట**: వింటేజ్ కార్లు, రాజ పల్లకీలు మరియు మధ్యయుగ ఆయుధాల మ్యూజియం కలిగిన రామ్‌నగర్ కోటను సందర్శించండి.",
                "**చునార్ కోట**: విక్రమార్క రాజు చేత గంగా నది ఒడ్డున నిర్మించబడిన రాతి కోటను సందర్శించండి.",
                "**జంతర్ మంతర్**: ఘాట్‌ల సమీపంలోని మాన్ మహల్ భవనం పైకప్పు పై నిర్మించిన ఖగోళ వేధశాలను సందర్శించండి.",
                "**భారత్ కళా భవన్**: బీహెచ్యూ (BHU) ఆవరణలోని పురాతన శిల్పాలు గల పురావస్తు మ్యూజియంను సందర్శించండి.",
                "**ఆలంగీర్ మసీదు**: హిందూ మరియు ఇస్లామిక్ నిర్మాణ శైలి మిశ్రమంతో ఔరంగజేబు నిర్మించిన చారిత్రక మసీదును సందర్శించండి.",
                "**మాన్ మందిర్ వేధశాల**: రాజా మాన్ సింగ్ చేత నిర్మించబడిన రాతి ఖగోళ పరికరాలు గల చారిత్రక ఘాట్ భవనాన్ని సందర్శించండి."
            ]
        },
        "default": {
            "en": [
                "**Dashashwamedh Ghat**: Explore the primary historical sites in Varanasi and see the evening Ganga Aarti ritual.",
                "**Ganga Sunrise Boat Ride**: Delight in local traditional street food (Kachori Jalebi, Lassi) and take an early morning boat ride.",
                "**Sarnath Trip & Shopping**: Pick up Banarasi Silk souvenirs from local bazaar areas and visit Sarnath stupas.",
                "**Kashi Vishwanath Temple**: Visit the gold-spired temple and stroll down Vishwanath Gali market paths.",
                "**Ramnagar Fort**: Visit the ancestral home of the Maharaja of Benares and try local Baati Chokha.",
                "**Banarasi Silk Weavers**: Spend a morning watching silk weavers work and shop at local markets.",
                "**Assi Ghat Yoga**: Experience the sunrise and participate in the Subah-e-Banaras morning yoga and music programs.",
                "**Bharat Kala Bhavan**: Visit the museum of art and archaeology inside the university campus."
            ],
            "hi": [
                "**दशाश्वमेध घाट**: वाराणसी के प्रमुख ऐतिहासिक स्थलों का भ्रमण करें और शाम की भव्य गंगा आरती अनुष्ठान देखें।",
                "**गंगा आरती और नौका विहार**: पारंपरिक व्यंजनों (कचौड़ी-जलेबी, लस्सी) का स्वाद लें और सुबह-सुबह नाव की सवारी करें।",
                "**सारनाथ और खरीदारी**: प्रसिद्ध बाजारों से बनारसी सिल्क की वस्तुएं खरीदें और सारनाथ स्तूपों का भ्रमण करें।",
                "**काशी विश्वनाथ मंदिर**: सोने के शिखर वाले मंदिर के दर्शन करें और विश्वनाथ गली के बाजार में घूमें।",
                "**रामनगर किला**: बनारस के महाराजा के पैतृक घर का दौरा करें और स्थानीय बाटी चोखा का स्वाद लें।",
                "**बनारसी सिल्क बुनकर**: सिल्क बुनकरों को काम करते हुए देखें और स्थानीय बाजारों में खरीदारी करें।",
                "**असि घाट योग**: सुबह की शुरुआत योग और संगीत कार्यक्रम 'सुबह-ए-बनारस' से करें।",
                "**भारत कला भवन**: विश्वविद्यालय परिसर के अंदर स्थित कला और पुरातात्विक संग्रहालय का दौरा करें।"
            ],
            "te": [
                "**దశాశ్వమేధ ఘాట్**: వారణాసి లోని ప్రధాన చారిత్రక ప్రదేశాలను సందర్శించి సాయంత్రం గంగా హారతిని వీక్షించండి.",
                "**గంగా సూర్యోదయ విహారం**: రుచికరమైన స్థానిక వంటకాలను (కచోరీ జిలేబీ, లస్సీ) ఆస్వాదించి ఉదయాన్నే పడవ ప్రయాణం చేయండి.",
                "**సార్నాథ్ & షాపింగ్**: బజార్ల నుండి బనారసి పట్టు చీరలను కొనుగోలు చేసి సార్నాథ్ స్థూపాలను సందర్శించండి.",
                "**కాశీ విశ్వనాథ ఆలయం**: సువర్ణ శిఖర ఆలయాన్ని సందర్శించి విశ్వనాథ్ గల్లీ బజార్లలో విహరించండి.",
                "**రామ్‌నగర్ కోట**: బెనారస్ మహారాజుల నివాసమైన రామ్‌నగర్ కోటను సందర్శించి స్థానిక బాటీ చోఖా రుచి చూడండి.",
                "**బనారసి చేనేత మగ్గాలు**: పట్టు వస్త్రాల చేనేత పనులను గమనించి స్థానిక దుకాణాలలో కొనుగోలు చేయండి.",
                "**అస్సి ఘాట్ యోగా**: సూర్యోదయ వేళ ఘాట్ వద్ద జరిగే 'సుబహ్-ఎ-బనారస్' ఉదయపు యోగా మరియు సంగీత వేడుకను అనుభవించండి.",
                "**భారత్ కళా భవన్**: యూనివర్సిటీ లోపల ఉండే చారిత్రక కళాఖండాల ప్రదర్శనశాలను సందర్శించండి."
            ]
        }
    },
    "jaipur": {
        "temples": {
            "en": [
                "**Govind Dev Ji Temple**: Attend the morning aarti at the beautiful Govind Dev Ji Temple, dedicated to Lord Krishna, inside the City Palace complex.",
                "**Birla Mandir**: Visit the modern white marble temple displaying fine carvings and serene atmosphere.",
                "**Galtaji**: Visit the historic temple in a mountain pass, famous for its natural fresh-water springs and monkeys.",
                "**Moti Dungri Temple**: Pay respects at the hilltop temple dedicated to Lord Ganesh, adjacent to Birla Mandir.",
                "**Garh Ganesh**: Climb up the hill to visit the ancient temple dedicated to Ganesha, offering panoramic views of Jaipur.",
                "**Akshardham**: Visit the modern temple complex showcasing intricate carvings, manicured lawns, and peace gardens.",
                "**Kale Hanuman Ji**: Visit the unique temple near Hawa Mahal featuring a black idol of Lord Hanuman.",
                "**Shila Devi Temple**: Visit the historic temple of the goddess inside the Amer Fort complex, built by Raja Man Singh."
            ],
            "hi": [
                "**गोविंद देव जी मंदिर**: सिटी पैलेस परिसर के अंदर भगवान कृष्ण को समर्पित सुंदर गोविंद देव जी मंदिर में सुबह की आरती में भाग लें।",
                "**बिड़ला मंदिर**: सुंदर नक्काशी और शांत वातावरण प्रदर्शित करने वाले आधुनिक सफेद संगमरमर के मंदिर के दर्शन करें।",
                "**गलताजी**: पहाड़ों के बीच स्थित ऐतिहासिक मंदिर का दौरा करें, जो अपने प्राकृतिक पानी के झरनों और बंदरों के लिए प्रसिद्ध है।",
                "**मोती डूंगरी मंदिर**: बिड़ला मंदिर के बगल में पहाड़ी पर स्थित भगवान गणेश को समर्पित मंदिर में माथा टेकें।",
                "**गढ़ गणेश**: जयपुर का मनोरम दृश्य प्रदान करने वाले गणेश जी के प्राचीन पहाड़ी मंदिर की चढ़ाई करें।",
                "**अक्षरधाम**: सुंदर नक्काशी, बगीचों और शांति उद्यानों को प्रदर्शित करने वाले आधुनिक मंदिर परिसर के दर्शन करें।",
                "**काले हनुमान जी**: हवा महल के पास स्थित अनोखे मंदिर के दर्शन करें जिसमें भगवान हनुमान की काली मूर्ति स्थापित है।",
                "**शिला देवी मंदिर**: राजा मान सिंह द्वारा निर्मित आमेर किले के भीतर स्थित ऐतिहासिक देवी मंदिर के दर्शन करें।"
            ],
            "te": [
                "**గోవింద దేవ్ జీ ఆలయం**: సిటీ ప్యాలెస్ కాంప్లెక్స్ లోపల శ్రీకృష్ణునికి అంకితం చేయబడిన సుందర గోవింద దేవ్ జీ ఆలయంలో ఉదయపు హారతిని వీక్షించండి.",
                "**బిర్లా మందిరం**: పాలరాతి శిల్పకళతో మరియు ప్రశాంతమైన వాతావరణంతో అలరారే ఆధునిక బిర్లా మందిరాన్ని సందర్శించండి.",
                "**గల్తాజీ**: కొండల మధ్య ఉన్న చారిత్రక ఆలయాన్ని సందర్శించండి, ఇది సహజమైన మంచినీటి కుండాలకు మరియు కోతులకు ప్రసిద్ధి.",
                "**మోతీ డూంగ్రీ ఆలయం**: బిర్లా మందిరానికి పక్కనే కొండపై ఉన్న వినాయకుడి ఆలయాన్ని సందర్శించండి.",
                "**గఢ్ గణేష్**: కొండపై ఉన్న పురాతన వినాయకుని ఆలయానికి నడక ద్వారా చేరుకుని జైపూర్ నగరం యొక్క సుందర దృశ్యాన్ని చూడండి.",
                "**అక్షరధామ్**: అద్భుతమైన శిల్పకళతో, పచ్చని తోటలతో నిండిన ఆధునిక దేవాలయ సముదాయాన్ని సందర్శించండి.",
                "**కాలే హనుమాన్ జీ**: హవా మహల్ సమీపంలో నల్లటి హనుమంతుని విగ్రహం గల ప్రత్యేక ఆలయాన్ని సందర్శించండి.",
                "**శిలా దేవి ఆలయం**: రాజా మాన్ సింగ్ చేత ఆమేర్ కోట లోపల ప్రతిష్టించబడిన చారిత్రక దేవి ఆలయాన్ని సందర్శించండి."
            ]
        },
        "food": {
            "en": [
                "**Kachori & Dal Baati**: Start with crispy Pyaz Kachori and Mirchi Bada. For dinner, experience the traditional Dal Baati Churma cooked with pure ghee.",
                "**Gatte ki Sabji**: Enjoy spicy Gatte ki Sabji and Ker Sangri curry at a traditional dining hall.",
                "**Lassiwala**: Grab a refreshing kulhad Lassi from Lassiwala on MI Road, and enjoy a traditional Rajasthani thali.",
                "**Rawat Mishthan Bhandar**: Taste the world-famous Mawa Kachori and hot onion kachoris.",
                "**Pandit Kulfi**: Visit the historic shop near Hawa Mahal for traditional saffron-flavored matka kulfis.",
                "**Sanjay Omelette**: Try unique, internationally featured local egg dishes and street snacks.",
                "**Masala Chowk**: Spend an evening sampling street foods from the city's legendary food stalls in one courtyard.",
                "**LMB Sweets**: Visit Lakshmi Mishthan Bhandar for traditional sweets like Paneer Ghevar and Royal Thali."
            ],
            "hi": [
                "**कचौड़ी और दाल बाटी**: स्थानीय मिठाई की दुकान पर खस्ता प्याज कचौड़ी और मिर्ची बड़ा का स्वाद लें। रात के भोजन में दाल बाटी चूरमा का स्वाद लें।",
                "**गट्टे की सब्जी**: एक पारंपरिक डाइनिंग हॉल में तीखी गट्टे की सब्जी और केर सांगरी करी का स्वाद लें।",
                "**लस्सीवाला**: एमआई रोड पर स्थित लस्सीवाला से ताजी कुल्हड़ लस्सी पिएं और पारंपरिक राजस्थानी शाही थाली का आनंद लें।",
                "**रावत मिष्ठान भंडार**: विश्व प्रसिद्ध मावा कचौड़ी और गरमा-गरम प्याज की कचौड़ी का स्वाद लें।",
                "**पंडित कुल्फी**: पारंपरिक केसर के स्वाद वाली मटका कुल्फी के लिए हवा महल के पास स्थित ऐतिहासिक दुकान पर जाएँ।",
                "**संजय ऑमलेट**: विभिन्न प्रकार के प्रसिद्ध स्थानीय अंडे के व्यंजनों और स्ट्रीट स्नैक्स का स्वाद लें।",
                "**मसाला चौक**: एक ही स्थान पर शहर के प्रसिद्ध स्टालों से विभिन्न प्रकार के स्ट्रीट फूड का स्वाद लें।",
                "**एलएमबी स्वीट्स**: लक्ष्मी मिष्ठान भंडार में पारंपरिक पनीर घेवर और राजस्थानी शाही थाली का आनंद लें।"
            ],
            "te": [
                "**కచోరీ & దాల్ బాటీ**: స్థానిక స్వీట్ షాపులో కరకరలాడే ప్యాజ్ కచోరీ మరియు మిర్చి బడాతో ప్రారంభించండి. రాత్రి విందుకు నెయ్యితో కూడిన సాంప్రదాయ దాల్ బాటీ చుర్మాను ఆస్వాదించండి.",
                "**గట్టే కీ సబ్జీ**: సంప్రదాయ భోజన శాలలో కారంగా ఉండే గట్టే కీ సబ్జీ మరియు కేర్ సాంగ్రీ కర్రీని ఆస్వాదించండి.",
                "**లస్సీవాలా**: ఎంఐ రోడ్డులోని లస్సీవాలా వద్ద లస్సీ తాగి, సాంప్రదాయ రాజస్థానీ రాజవిందును ఆస్వాదించండి.",
                "**రావత్ మిష్టాన్ భండార్**: ఇక్కడి ప్రసిద్ధ మావా కచోరీ మరియు వేడివేడి ఉల్లిపాయ కచోరీలను రుచి చూడండి.",
                "**పండిట్ కుల్ఫీ**: హవా మహల్ సమీపంలో ఉండే ఈ చారిత్రక షాపులో కుండ కుల్ఫీని తప్పకుండా ప్రయత్నించండి.",
                "**సంజయ్ ఆమ్లెట్**: అంతర్జాతీయంగా గుర్తింపు పొందిన ఇక్కడి రకరకాల కోడిగుడ్డు వంటకాలను మరియు స్నాక్స్ ని రుచి చూడండి.",
                "**మసాలా చౌక్**: నగరంలోని ప్రసిద్ధ వీధి వంటకాలన్నీ ఒకే చోట లభించే మసాలా చౌక్ లో సాయంత్రం గడపండి.",
                "**LMB స్వీట్స్**: లక్ష్మీ మిష్టాన్ భండార్ లో లభించే పనీర్ ఘేవార్ మరియు రాజస్థానీ రాయల్ భోజనాన్ని ఆస్వాదించండి."
            ]
        },
        "nature": {
            "en": [
                "**Kanak Vrindavan**: Relax in the beautifully landscaped gardens situated at the valley foot of Nahargarh hills.",
                "**Jhalana Leopard Safari**: Experience a thrilling open-jeep safari through the scenic wilderness, famous for leopard sightings.",
                "**Central Park**: Walk through the largest public park in Jaipur, featuring green lawns and musical fountains.",
                "**Ram Niwas Garden**: Stroll around the historic 19th-century public park featuring green lawns and Albert Hall.",
                "**Sisodia Rani Garden**: Visit the terraced gardens decorated with fountains, water courses, and murals of Radha-Krishna.",
                "**Vidyadhar Garden**: Explore the peaceful garden displaying fine landscaping and traditional stone work.",
                "**Sambhar Salt Lake**: Day trip to India's largest inland salt lake, great for bird-watching and sunset views.",
                "**Chandlai Lake**: Visit the quiet lake on the outskirts of Jaipur, a hotspot for migratory birds like flamingos."
            ],
            "hi": [
                "**कनक वृंदावन घाटी**: नाहरगढ़ पहाड़ियों की घाटी में स्थित सुंदर और नक्काशीदार बगीचों में आराम करें।",
                "**झालाना तेंदुआ सफारी**: तेंदुए को देखने के लिए प्रसिद्ध सुंदर जंगलों के बीच एक रोमांचक खुली जीप सफारी का अनुभव करें।",
                "**सेंट्रल पार्क**: जयपुर के सबसे बड़े पार्क में घूमें, जिसमें हरे-भरे मैदान और संगीमतय फव्वारे हैं।",
                "**राम निवास बाग**: ऐतिहासिक 19वीं शताब्दी के पार्क में टहलें, जिसमें सुंदर मैदान और अल्बर्ट हॉल शामिल हैं।",
                "**सिसोदिया रानी बाग**: फव्वारों, जलमार्गों और राधा-कृष्ण के भित्तिचित्रों से सजे सुंदर बगीचे का दौरा करें।",
                "**विद्याधर बाग**: बेहतरीन भूदृश्य और पारंपरिक पत्थर के काम को प्रदर्शित करने वाले शांत बगीचे का अन्वेषण करें।",
                "**सांभर नमक झील**: भारत की सबसे बड़ी अंतर्देशीय नमक झील की सैर करें, जो पक्षियों को देखने और सूर्यास्त के लिए प्रसिद्ध है।",
                "**चांदलई झील**: जयपुर के बाहरी इलाके में स्थित शांत झील पर जाएं, जो राजहंस (फ्लेमिंगो) जैसे प्रवासी पक्षियों का घर है।"
            ],
            "te": [
                "**కనక బృందావనం**: నహర్‌గఢ్ కొండల దిగువన ఉన్న అందమైన తోటలలో విశ్రాంతి తీసుకోండి.",
                "**ఝలానా లెపార్డ్ సఫారీ**: చిరుత పులులకు ప్రసిద్ధి చెందిన అడవిలో థ్రిల్లింగ్ ఓపెన్-జీప్ సఫారీని అనుభవించండి.",
                "**సెంట్రల్ పార్క్**: పచ్చని లాన్లు, ఎత్తైన చెట్లు మరియు మ్యూజికల్ ఫౌంటైన్లతో కూడిన జైపూర్‌లోని అతిపెద్ద పార్కులో విహరించండి.",
                "**రామ్ నివాస్ గార్డెన్**: ఆల్బర్ట్ హాల్ మ్యూజియం కలిగిన చారిత్రక 19వ శతాబ్దపు పార్కులో సాయంత్రం నడకను ఆస్వాదించండి.",
                "**సిసోడియా రాణి తోట**: అందమైన జలపాతాలు, ఫౌంటైన్లు మరియు రాధాకృష్ణుల చిత్రాలతో అలంకరించబడిన ఉద్యానవనాన్ని సందర్శించండి.",
                "**విద్యాధర్ గార్డెన్**: అద్భుతమైన నిర్మాణ శైలి మరియు ప్రశాంతమైన వాతావరణం కలిగిన ఈ తోటను సందర్శించండి.",
                "**సాంబార్ ఉప్పు సరస్సు**: భారతదేశంలోనే అతిపెద్దదైన సాంబార్ సరస్సును సందర్శించి సూర్యాస్తమయాన్ని వీక్షించండి.",
                "**చాంద్‌లై సరస్సు**: వలస పక్షులు, ముఖ్యంగా ఫ్లెమింగోలు వచ్చే జైపూర్ శివార్లలోని ప్రశాంతమైన చెరువును సందర్శించండి."
            ]
        },
        "shopping": {
            "en": [
                "**Johari Bazar**: Shop at Johari Bazar, world-famous for Meenakari jewelry, gold, and hand-cut gemstones.",
                "**Bapu Bazar**: Explore Bapu Bazar and Nehru Bazar for colorful bandhani sarees, block-printed textiles, and mojris (leather shoes).",
                "**Craft Workshops**: Visit local artisan workshops outside the city to see blue pottery and hand-block printing techniques.",
                "**Tripolia Bazar**: Shop for traditional lac bangles, brassware, iron utensils, and local crafts.",
                "**Chandpole Bazar**: Explore the busy streets famous for marble sculptures, stone carvings, and traditional handicrafts.",
                "**Kishanpole Bazar**: Shop for high-quality wooden furniture, block-printed fabrics, and tie-dye textiles.",
                "**Sireh Deori Bazar**: Browse the stalls opposite Hawa Mahal for leather puppets, wall hangings, and camel leather items.",
                "**Nehru Bazar**: Shop for traditional mojris, colorful bags, and ethnic garments at bargain prices."
            ],
            "hi": [
                "**जौहरी बाजार**: मीनाकारी आभूषणों, सोने और रत्नों के लिए विश्व प्रसिद्ध जौहरी बाजार में शानदार खरीदारी करें।",
                "**बापू बाजार**: बापू बाजार से रंग-बिरंगी बंधेज साड़ियाँ, ब्लॉक-प्रिंटेड कपड़े और पारंपरिक राजस्थानी मोजरी (चमड़े के जूते) खरीदें।",
                "**शिल्प कार्यशालाएं**: नीले बर्तन (ब्लू पॉटरी) और लकड़ी के ब्लॉक प्रिंट बनाने की कला देखने के लिए स्थानीय कारीगरों की कार्यशालाओं का दौरा करें।",
                "**त्रिपोलिया बाजार**: पारंपरिक लाख की चूड़ियों, पीतल के बर्तनों, लोहे के बर्तनों और स्थानीय शिल्प की खरीदारी करें।",
                "**चांदपोल बाजार**: संगमरमर की मूर्तियों, पत्थर की नक्काशी और पारंपरिक हस्तशिल्प के लिए प्रसिद्ध व्यस्त सड़कों का अन्वेषण करें।",
                "**किशनपोल बाजार**: उच्च गुणवत्ता वाले लकड़ी के फर्नीचर, ब्लॉक-प्रिंटेड कपड़े और बांधनी वस्त्रों की खरीदारी करें।",
                "**सिरेह देओरी बाजार**: चमड़े की कठपुतली, दीवार पर लटकने वाली सजावट और ऊंट के चमड़े के सामानों की खरीदारी करें।",
                "**नेहरू बाजार**: पारंपरिक मोजरी, रंग-बिरंगे बैग और जातीय परिधानों की खरीदारी करें।"
            ],
            "te": [
                "**జోహరీ బజార్**: మీనాకారీ ఆభరణాలు, బంగారం మరియు రత్నాలకు ప్రపంచ ప్రసిద్ధి చెందిన జోహరీ బజార్‌లో షాపింగ్ చేయండి.",
                "**బాపు బజార్**: బాపు బజార్‌లో రంగురంగుల బంధాని చీరలు, బ్లాక్-ప్రింట్ దుస్తులు మరియు సాంప్రదాయ రాజస్థానీ మోజ్రీలను (తోలు బూట్లు) కొనుగోలు చేయండి.",
                "**హస్తకళల వర్క్‌షాప్‌లు**: ప్రసిద్ధ బ్లూ పాటరీ మరియు చేతితో తయారు చేసే వుడెన్ బ్లాక్ ప్రింట్ తయారీని చూడటానికి స్థానిక కళాకారుల వర్క్‌షాప్‌లను సందర్శించండి.",
                "**త్రిపోలియా బజార్**: ఇక్కడి సాంప్రదాయ లక్ష గాజులు, ఇత్తడి వస్తువులు మరియు లోహపు హస్తకళల వస్తువులను కొనుగోలు చేయండి.",
                "**చాంద్‌పోల్ బజార్**: పాలరాతి విగ్రహాలు, రాతి శిల్పాలు మరియు సాంప్రదాయ వస్తువుల అమ్మకాలకు ప్రసిద్ధి చెందిన వీధులను సందర్శించండి.",
                "**కిషన్‌పోల్ బజార్**: నాణ్యమైన చెక్క ఫర్నిచర్, బ్లాక్-ప్రింట్ బట్టలు మరియు కలంకారీ దుస్తులను కొనుగోలు చేయండి.",
                "**సిరేహ్ దేవి బజార్**: హవా మహల్ ఎదురుగా లభించే తోలు బొమ్మలు, గోడ అలంకరణ వస్తువులు మరియు ఒంటె తోలు ఉత్పత్తులను షాపింగ్ చేయండి.",
                "**నెహ్రూ బజార్**: రంగురంగుల బ్యాగులు, రాజస్థానీ మోజ్రీలు మరియు సాంప్రదాయ బట్టల షాపింగ్ కోసం ఇక్కడికి వెళ్ళండి."
            ]
        },
        "history": {
            "en": [
                "**Amer Fort**: Explore Amer Fort (Sheesh Mahal, Ganesh Pol) with its majestic architecture.",
                "**Hawa Mahal**: Visit the Hawa Mahal (Palace of Breeze), City Palace, and the ancient Jantar Mantar observatory.",
                "**Albert Hall**: Tour the Albert Hall Museum and catch a stunning sunset from Nahargarh Fort.",
                "**Jaigarh Fort**: Visit the fort housing the massive Jaivana Cannon, the world's largest cannon on wheels.",
                "**Jal Mahal**: Admire the beautiful palace floating in the middle of Man Sagar Lake.",
                "**Jantar Mantar**: Discover the UNESCO site featuring the world's largest stone sundial and astronomical instruments.",
                "**Gaitore Cenotaphs**: Visit the peaceful resting place of Jaipur's royal rulers, decorated with stone carvings.",
                "**Bhangarh Fort**: Take an adventurous day excursion to the historic 17th-century fort ruins, known for local mysteries."
            ],
            "hi": [
                "**आमेर किला**: शानदार वास्तुकला वाले आमेर किले (शीश महल, गणेश पोल) का अन्वेषण करें।",
                "**हवा महल**: हवा महल (पैलेस ऑफ ब्रीज), सिटी पैलेस और प्राचीन जंतर-मंतर वेधशाला का दौरा करें।",
                "**अल्बर्ट हॉल**: अल्बर्ट हॉल संग्रहालय का दौरा करें और नाहरगढ़ किले से सूर्यास्त का सुंदर दृश्य देखें।",
                "**जयगढ़ किला**: पहियों पर दुनिया की सबसे बड़ी तोप 'जयबाण तोप' वाले ऐतिहासिक किले का दौरा करें।",
                "**जल महल**: मान सागर झील के बीच तैरते हुए सुंदर महल की भव्यता की प्रशंसा करें।",
                "**जंतर मंतर**: दुनिया की सबसे बड़ी पत्थर की धूपघड़ी वाले यूनेस्को विरासत स्थल का अन्वेषण करें।",
                "**गैटोर की छतरियां**: पत्थर की नक्काशी से सजे जयपुर के शाही शासकों के शांतिपूर्ण विश्राम स्थल का दौरा करें।",
                "**भानगढ़ किला**: स्थानीय रहस्यों के लिए प्रसिद्ध ऐतिहासिक 17वीं सदी के किले के खंडहरों की साहसिक सैर करें।"
            ],
            "te": [
                "**ఆమేర్ కోట**: ఆమేర్ కోటలోని శీష్ మహల్, గణేష్ పోల్ వంటి అద్భుతమైన నిర్మాణ శైలిని గమనించండి.",
                "**హవా మహల్**: 953 కిటికీలు ఉన్న హవా మహల్, సిటీ ప్యాలెస్ మరియు పురాతన జంతర్ మంతర్ ఖగోళ వేధశాలను సందర్శించండి.",
                "**ఆల్బర్ట్ హాల్**: ఆల్బర్ట్ హాల్ మ్యూజియంను సందర్శించి, నహర్‌గఢ్ కోట పై నుండి పింక్ సిటీ సూర్యాస్తమయ దృశ్యాన్ని తిలకించండి.",
                "**జైగఢ్ కోట**: చక్రాలపై ఉన్న ప్రపంచంలోనే అతిపెద్ద తోపు 'జైబాణ తోపు'ను జైగఢ్ కోటలో చూడండి.",
                "**జల్ మహల్**: మాన్ సాగర్ సరస్సు మధ్యలో తేలియాడుతున్నట్లు కన్పించే సుందరమైన జల్ మహల్ ను వీక్షించండి.",
                "**జంతర్ మంతర్**: ప్రపంచంలోనే అతిపెద్ద రాతి సూర్య గడియారం గల యునెస్కో హెరిటేజ్ సైట్ ను సందర్శించండి.",
                "**గైటోర్ సమాధులు**: అద్భుతమైన శిల్పకళతో చెక్కబడిన జైపూర్ రాజుల రాజవంశ సమాధులను సందర్శించండి.",
                "**భానగఢ్ కోట**: రాత్రి పూట ప్రవేశం లేని, అనేక కథలతో ప్రసిద్ధి చెందిన భానగఢ్ కోట శిథిలాలను సందర్శించండి."
            ]
        },
        "default": {
            "en": [
                "**Amer Fort**: Explore the primary historical forts in Jaipur and see the magnificent architecture.",
                "**Hawa Mahal & Food**: Delight in traditional Rajasthani food (Pyaz Kachori, Ghevar) and visit Hawa Mahal.",
                "**Bapu Bazar & Shopping**: Pick up traditional block-print sarees and mojris from bazaar areas.",
                "**City Palace**: Visit the palace complex with its grand courtyards and royal museum exhibits.",
                "**Jantar Mantar**: Explore the collection of architectural astronomical instruments.",
                "**Nahargarh Fort**: Drive up to the fort for a stunning panoramic sunset view of the pink city.",
                "**Jal Mahal**: Take a walk along the lakeside and photograph the floating palace.",
                "**Chokhi Dhani**: Spend an evening experiencing traditional Rajasthani folk dance, camel rides, and local dining."
            ],
            "hi": [
                "**आमेर किला**: जयपुर के प्रमुख ऐतिहासिक किलों का भ्रमण करें और शानदार वास्तुकला देखें।",
                "**हवा महल और भोजन**: पारंपरिक राजस्थानी व्यंजनों (प्याज कचौड़ी, घेवर) का आनंद लें और हवा महल घूमें।",
                "**बापू बाजार और खरीदारी**: प्रसिद्ध बाजारों से पारंपरिक ब्लॉक-प्रिंट साड़ियाँ और मोजरी खरीदें।",
                "**सिटी पैलेस**: भव्य आंगनों और शाही संग्रहालय प्रदर्शनियों वाले महल परिसर का दौरा करें।",
                "**जंतर मंतर**: वास्तुकला खगोलीय उपकरणों के संग्रह का अन्वेषण करें।",
                "**नाहरगढ़ किला**: गुलाबी शहर के सूर्यास्त का सुंदर दृश्य देखने के लिए किले की यात्रा करें।",
                "**जल महल**: झील के किनारे टहलें और पानी पर तैरते महल की तस्वीरें लें।",
                "**चोखी ढाणी**: पारंपरिक राजस्थानी लोक नृत्य, ऊंट की सवारी और स्थानीय भोजन का आनंद लें।"
            ],
            "te": [
                "**ఆమేర్ కోట**: జైపూర్ లోని ప్రధాన చారిత్రక కోటలను సందర్శించి అద్భుతమైన నిర్మాణ శైలిని గమనించండి.",
                "**హవా మహల్ & వంటకాలు**: సాంప్రదాయ రాజస్థానీ వంటకాలను (ప్యాజ్ కచోరీ, ఘేవార్) ఆస్వాదించి హవా మహల్ సందర్శించండి.",
                "**బాపు బజార్ & షాపింగ్**: బజార్ల నుండి సాంప్రదాయ బ్లాక్-ప్రింట్ చీరలు మరియు మోజ్రీలను కొనుగోలు చేయండి.",
                "**సిటీ ప్యాలెస్**: రాజకుటుంబ మ్యూజియంలు మరియు విశాలమైన ప్రాంగణాలు గల సిటీ ప్యాలెస్ ను సందర్శించండి.",
                "**జంతర్ మంతర్**: రాతితో నిర్మించిన చారిత్రక ఖగోళ ఉపకరణాల సముదాయాన్ని అన్వేషించండి.",
                "**నహర్‌గఢ్ కోట**: నగర సూర్యాస్తమయ సుందర దృశ్యాన్ని వీక్షించడానికి కొండపై గల నహర్‌గఢ్ కోటకు వెళ్ళండి.",
                "**జల్ మహల్**: సాయంత్రం సరస్సు గట్టు వెంబడి నడుస్తూ నీటిపై వెలిగిపోయే జల్ మహల్ ఫోటోలు తీసుకోండి.",
                "**చోకీ ధానీ**: రాజస్థానీ జానపద నృత్యాలు, ఒంటె సవారీలు మరియు సాంప్రదాయ విందు గల చోకీ ధానీ విలేజ్ లో సాయంత్రం గడపండి."
            ]
        }
    },
    "mumbai": {
        "temples": {
            "en": [
                "**Siddhivinayak**: Visit the famous temple dedicated to Lord Ganesha, a spiritual landmark.",
                "**Mahalakshmi**: Visit the scenic temple by the sea, dedicated to Goddess Lakshmi.",
                "**Babulnath**: Explore the ancient hilltop temple dedicated to Lord Shiva.",
                "**Mumba Devi**: Visit the historic temple of the city's patron goddess, from whom Mumbai gets its name.",
                "**ISKCON Juhu**: Explore the grand temple complex showcasing beautiful paintings and spiritual library.",
                "**Walkeshwar Temple**: Visit the historic temple near the sacred Banganga Tank in South Mumbai.",
                "**Mount Mary Basilica**: Visit the historic Roman Catholic church on a hill in Bandra, offering sea views.",
                "**Global Vipassana Pagoda**: Visit the massive meditation dome near Gorai, promoting inner peace."
            ],
            "hi": [
                "**सिद्धिविनायक**: भगवान गणेश को समर्पित प्रसिद्ध मंदिर के दर्शन करें, जो एक आध्यात्मिक पहचान है।",
                "**महालक्ष्मी**: समुद्र के किनारे स्थित सुंदर मंदिर के दर्शन करें, जो देवी लक्ष्मी को समर्पित है।",
                "**बाबुलनाथ**: भगवान शिव को समर्पित प्राचीन पहाड़ी मंदिर का अन्वेषण करें।",
                "**मुम्बा देवी**: शहर की संरक्षक देवी के ऐतिहासिक मंदिर के दर्शन करें, जिनके नाम पर मुंबई का नाम पड़ा है।",
                "**इस्कॉन जुहू**: सुंदर चित्रों और आध्यात्मिक पुस्तकालय को प्रदर्शित करने वाले भव्य मंदिर परिसर का भ्रमण करें।",
                "**वाल्केश्वर मंदिर**: दक्षिण मुंबई में पवित्र बाणगंगा टैंक के पास स्थित ऐतिहासिक मंदिर के दर्शन करें।",
                "**माउंट मैरी बेसिलिका**: बांद्रा की पहाड़ी पर स्थित ऐतिहासिक चर्च के दर्शन करें, जो समुद्र का सुंदर दृश्य प्रदान करता है।",
                "**ग्लोबल विपश्यना पैगोडा**: आंतरिक शांति को बढ़ावा देने वाले गोराई के पास स्थित विशाल ध्यान गुंबद के दर्शन करें।"
            ],
            "te": [
                "**సిద్ధి వినాయక ఆలయం**: వినాయకునికి అంకితం చేయబడిన అత్యంత ప్రసిద్ధ మరియు చారిత్రక ఆలయాన్ని సందర్శించండి.",
                "**మహాలక్ష్మి దేవాలయం**: సముద్ర తీరంలో వెలసిన లక్ష్మీ దేవి ఆలయాన్ని సందర్శించండి.",
                "**బాబుల్‌నాథ్ ఆలయం**: కొండపై ఉన్న పురాతన శివాలయాన్ని సందర్శించి ఆధ్యాత్మిక ప్రశాంతతను పొందండి.",
                "**ముంబా దేవి ఆలయం**: ముంబై నగరానికి ఆ పేరు రావడానికి కారణమైన ఇక్కడి గ్రామదేవత ఆలయాన్ని సందర్శించండి.",
                "**ఇస్కాన్ జుహూ**: జుహూ లోని అందమైన శ్రీకృష్ణ మందిరాన్ని మరియు దాని ప్రశాంత వాతావరణాన్ని అన్వేషించండి.",
                "**వాకేశ్వర్ ఆలయం**: దక్షిణ ముంబై లోని పవిత్ర బాణగంగ కోనేరు సమీపంలో గల చారిత్రక శివాలయాన్ని సందర్శించండి.",
                "**మౌంట్ మేరీ బాసిలికా**: సముద్ర తీరం వెంబడి ఉండే బాంద్రాలోని చారిత్రక రోమన్ కాథలిక్ చర్చిని సందర్శించండి.",
                "**గ్లోబల్ విపస్సన పగోడా**: ప్రశాంతమైన ధ్యానం కోసం గోరై వద్ద నిర్మించిన భారీ స్థూపాన్ని సందర్శించండి."
            ]
        },
        "food": {
            "en": [
                "**Vada Pav**: Try local street food, the legendary deep-fried potato dumpling in bun.",
                "**Pav Bhaji**: Eat butter-rich Pav Bhaji at the iconic street stalls on Girgaon Chowpatty beach.",
                "**Irani Cafe**: Drink hot bun maska and specialty tea at legendary spots like Kyani & Co.",
                "**Keema Ghotala**: Sample the traditional spiced minced meat dish at Cafe Haji Ali or BadeMiya.",
                "**Mohammad Ali Road**: Experience a late-night street food walk tasting spicy seekh kebabs and sweets.",
                "**Seafood Feast**: Try authentic Mangalorean fish curry and butter garlic crab at Mahesh Lunch Home.",
                "**Badshah Falooda**: Relish the famous rose-flavored falooda ice cream dessert near Crawford Market.",
                "**Amar Juice Centre**: Try local fusion street snacks, cheese pav bhaji, and fruit juices."
            ],
            "hi": [
                "**वड़ा पाव**: स्थानीय स्ट्रीट फूड का आनंद लें, जो बन में तला हुआ आलू का वड़ा है।",
                "**पाव भाजी**: गिरगांव चौपाटी समुद्र तट पर स्थित प्रसिद्ध स्टालों पर मक्खन से भरपूर पाव भाजी खाएं।",
                "**इरानी कैफे**: क्यानी एंड कंपनी जैसे ऐतिहासिक स्थानों पर मलाईदार बन मस्का और ईरानी चाय का आनंद लें।",
                "**कीमा घोटाला**: कैफे हाजी अली या बड़ेमिया में पारंपरिक मसालेदार कीमा व्यंजन का स्वाद लें।",
                "**मोहम्मद अली रोड**: रात के समय तीखे सीख कबाब और मिठाइयों का स्वाद लेने के लिए स्ट्रीट फूड वॉक का अनुभव करें।",
                "**सीफूड दावत**: महेश लंच होम में मैंगलोरियन शैली की मछली करी और बटर गार्लिक केकड़े का स्वाद लें।",
                "**बादशाह फालूदा**: क्रॉफर्ड मार्केट के पास प्रसिद्ध गुलाब के स्वाद वाले फालूदा आइसक्रीम डेजर्ट का आनंद लें।",
                "**अमर जूस सेंटर**: स्थानीय फ्यूजन स्ट्रीट स्नैक्स, चीज पाव भाजी और फलों के जूस का स्वाद लें।"
            ],
            "te": [
                "**వడా పావ్**: ముంబై యొక్క ఐకానిక్ వీధి ఆహారమైన వేడి వేడి వడా పావ్ ని ఆస్వాదించండి.",
                "**పావ్ భాజీ**: గిర్గావ్ చౌపాతీ బీచ్ లో లభించే వెన్నతో కూడిన రుచికరమైన పావ్ భాజీని తినండి.",
                "**ఇరానీ కేఫ్**: క్యానీ అండ్ కో వంటి పురాతన కేఫ్‌లలో బన్ మస్కా మరియు ఇరానీ చాయ్ తాగండి.",
                "**ఖీమా ఘోటాల**: స్థానిక మసాలా వంటకం ఖీమా ఘోటాలను హాజీ అలీ కేఫ్ వద్ద రుచి చూడండి.",
                "**మహ్మద్ అలీ రోడ్డు**: రాత్రి పూట లభించే కారంగా ఉండే కబాబ్స్ మరియు స్వీట్ల వీధి ఆహార విహారాన్ని అనుభవించండి.",
                "**సీఫుడ్ విందు**: మహేష్ లంచ్ హోమ్ లో లభించే సాంప్రదాయ మంగళూరు చేపల పులుసును ప్రయత్నించండి.",
                "**బాద్షా ఫలూదా**: క్రాఫోర్డ్ మార్కెట్ సమీపంలో లభించే ప్రసిద్ధ రోజ్ ఫ్లేవర్ ఫలూదా ఐస్ క్రీంను రుచి చూడండి.",
                "**అమర్ జ్యూస్ సెంటర్**: ఇక్కడి చీజ్ పావ్ భాజీ మరియు తాజా పండ్ల రసాలను ప్రయత్నించండి."
            ]
        },
        "nature": {
            "en": [
                "**Sanjay Gandhi National Park**: Explore the green reserve within city limits with mini safaris.",
                "**Marine Drive**: Take a stroll along the promenade to view a spectacular sunset by the sea.",
                "**Hanging Gardens**: Relax in the terraced gardens on Malabar Hill offering animal-shaped hedges.",
                "**Juhu Beach**: Walk along the popular beach, taking in the sea breeze and sunset views.",
                "**Gorai Beach**: Take a ferry to the quiet and sandy beach on the outskirts, perfect for relaxation.",
                "**Sewri Mudflats**: Visit the mudflats to watch migratory pink flamingos during the winter months.",
                "**Yeoor Hills**: Hike up the scenic forest trails located inside the Sanjay Gandhi National Park buffer zone.",
                "**Priyadarshini Park**: Stroll in the green coastal park featuring jogging tracks and sea views."
            ],
            "hi": [
                "**संजय गांधी राष्ट्रीय उद्यान**: मिनी सफारी के साथ शहर की सीमा के भीतर स्थित इस हरित रिजर्व का अन्वेषण करें।",
                "**मरीन ड्राइव**: समुद्र के किनारे एक शानदार सूर्यास्त देखने के लिए सैरगाह पर टहलें।",
                "**हैंगिंग गार्डन**: मालाबार हिल पर स्थित बगीचे में आराम करें, जहां जानवरों के आकार की झाड़ियां हैं।",
                "**जुहू बीच**: समुद्र की हवा और सूर्यास्त के दृश्यों का आनंद लेते हुए लोकप्रिय समुद्र तट पर टहलें।",
                "**गोराई बीच**: बाहरी इलाके में स्थित शांत और रेतीले समुद्र तट के लिए एक नौका यात्रा करें।",
                "**शिवड़ी मडफ्लैट्स**: सर्दियों के महीनों के दौरान आने वाले गुलाबी राजहंसों (फ्लेमिंगो) को देखने के लिए मडफ्लैट्स पर जाएँ।",
                "**यूर हिल्स**: राष्ट्रीय उद्यान के आरक्षित क्षेत्र में स्थित सुंदर वन मार्गों पर ट्रेकिंग करें।",
                "**प्रियदर्शिनी पार्क**: जॉगिंग ट्रैक और समुद्र के दृश्यों वाले इस तटीय पार्क में टहलें।"
            ],
            "te": [
                "**సంజయ్ గాంధీ నేషనల్ పార్క్**: నగర సరిహద్దుల్లోనే ఉన్న పచ్చని అడవిని మరియు అక్కడి కన్హేరి గుహలను అన్వేషించండి.",
                "**మెరైన్ డ్రైవ్**: సముద్ర తీరం వెంబడి నడుస్తూ సుందరమైన సూర్యాస్తమయ దృశ్యాన్ని తిలకించండి.",
                "**హ్యాంగింగ్ గార్డెన్స్**: మలబార్ హిల్స్ పై జంతువుల ఆకృతిలో కత్తిరించిన చెట్లు గల అందమైన తోటలలో విశ్రాంతి తీసుకోండి.",
                "**జుహూ బీచ్**: సముద్రపు గాలిని మరియు ఇసుక తిన్నెలను ఆస్వాదిస్తూ బీచ్ వెంబడి నడవండి.",
                "**గోరై బీచ్**: ప్రశాంతమైన మరియు ఇసుకతో కూడిన సముద్ర తీరానికి పడవ ప్రయాణం చేయండి.",
                "**సెవ్రీ మడ్‌ఫ్లాట్స్**: చలికాలంలో ఇక్కడికి వలస వచ్చే అందమైన గులాబీ రంగు ఫ్లెమింగో పక్షులను వీక్షించండి.",
                "**యేవూర్ కొండలు**: థానే సమీపంలో ఉండే అందమైన అడవి కొండలలో లఘు ట్రెకింగ్ చేయండి.",
                "**ప్రియదర్శిని పార్క్**: సముద్ర తీరం వెంబడి ఉండే పచ్చని పార్కులో సాయంత్రం నడకను ఆస్వాదించండి."
            ]
        },
        "shopping": {
            "en": [
                "**Colaba Causeway**: Shop for antique jewelry, handicrafts, books, and trendy apparel.",
                "**Linking Road**: Explore the bustling streets of Bandra for trendy clothes and budget footwear.",
                "**Crawford Market**: Visit the historic market for wholesale spices, dry fruits, and gifts.",
                "**Fashion Street**: Browse the long row of stalls near CST for export-surplus clothing at cheap prices.",
                "**Chor Bazaar**: Shop for vintage objects, old gramophones, antique furniture, and unique curios.",
                "**Zaveri Bazar**: Explore the busy jewelry hub famous for gold, diamonds, and traditional silver ornaments.",
                "**Mangaldas Market**: Visit the historic indoor fabric market for traditional block prints and silks.",
                "**Hill Road**: Explore the lively street shopping strip in Bandra for boutique fashion."
            ],
            "hi": [
                "**कोलाबा कॉजवे**: प्राचीन आभूषणों, हस्तशिल्प, पुस्तकों और कपड़ों की खरीदारी करें।",
                "**लिंकिंग रोड**: ट्रेंडी कपड़ों और बजट जूते-चप्पलों के लिए बांद्रा की व्यस्त सड़कों का अन्वेषण करें।",
                "**क्रॉफर्ड मार्केट**: थोक मसालों, सूखे मेवों और उपहारों के लिए ऐतिहासिक बाजार का दौरा करें।",
                "**फैशन स्ट्रीट**: सस्ते दामों पर ट्रेंडी कपड़ों के लिए सीएसटी के पास स्टालों की लंबी कतार देखें।",
                "**चोर बाजार**: पुरानी वस्तुओं, पुराने ग्रामोफोन, प्राचीन फर्नीचर और अनूठी कलाकृतियों की खरीदारी करें।",
                "**जवेरी बाजार**: सोने, हीरे और पारंपरिक चांदी के गहनों के लिए प्रसिद्ध आभूषण बाजार का दौरा करें।",
                "**मंगलदास मार्केट**: पारंपरिक ब्लॉक प्रिंट और रेशम के कपड़ों के लिए कपड़ा बाजार का दौरा करें।",
                "**हिल रोड**: बुटीक फैशन के लिए बांद्रा में जीवंत स्ट्रीट शॉपिंग का आनंद लें।"
            ],
            "te": [
                "**కోలాబా కాజ్‌వే**: పురాతన ఆభరణాలు, హస్తకళల వస్తువులు మరియు దుస్తుల కొనుగోలు కోసం ఇక్కడికి వెళ్ళండి.",
                "**లింకింగ్ రోడ్**: బాంద్రాలోని అత్యంత సందడి గల బట్టలు మరియు చెప్పుల మార్కెట్ ను సందర్శించండి.",
                "**క్రాఫోర్డ్ మార్కెట్**: నాణ్యమైన మసాలా దినుసులు, డ్రై ఫ్రూట్స్ కొనుగోలు కోసం ఈ చారిత్రక మార్కెట్ ను సందర్శించండి.",
                "**ఫ్యాషన్ స్ట్రీట్**: అతి తక్కువ ధరలలో లభించే దుస్తుల కోసం సిఎస్టి స్టేషన్ సమీపంలోని వీధి దుకాణాలను సందర్శించండి.",
                "**చోర్ బజార్**: పాత సామాగ్రి, వింటేజ్ వస్తువులు మరియు పురాతన ఫర్నిచర్ కోసం ఈ మార్కెట్ ని సందర్శించండి.",
                "**జవేరి బజార్**: బంగారం మరియు వెండి ఆభరణాలకు ప్రసిద్ధి చెందిన జవేరి బజార్‌లో షాపింగ్ చేయండి.",
                "**మంగళదాస్ మార్కెట్**: వివిధ రకాల వస్త్రాలు మరియు బ్లాక్ ప్రింట్ దుస్తుల హోల్‌సేల్ మార్కెట్‌ను సందర్శించండి.",
                "**హిల్ రోడ్**: బాంద్రాలోని ప్రసిద్ధ వీధి మార్కెట్లో ఆధునిక ఫ్యాషన్ దుస్తులను కొనుగోలు చేయండి."
            ]
        },
        "history": {
            "en": [
                "**Elephanta Caves**: Take a scenic ferry ride to see the ancient rock-cut cave temples.",
                "**CSMT**: Admire the Victorian Gothic Revival architecture of the UNESCO heritage railway station.",
                "**Mani Bhavan**: Visit Mahatma Gandhi's former residence, now a museum containing historic letters.",
                "**Gateway of India**: View the grand monument built to commemorate the visit of King George V.",
                "**Kanheri Caves**: Explore the ancient Buddhist rock-cut caves located inside Sanjay Gandhi National Park.",
                "**Vasai Fort**: Take a day trip to explore the massive ruins of the Portuguese fort on the coast.",
                "**Haji Ali Dargah**: Visit the 15th-century mosque located on an islet off the coast of Worli.",
                "**Bhau Daji Lad Museum**: Explore Mumbai's oldest museum displaying decorative arts and clay models."
            ],
            "hi": [
                "**एलीफेंटा की गुफाएं**: प्राचीन चट्टानों को काटकर बनाए गए गुफा मंदिरों को देखने के लिए नौका विहार का आनंद लें।",
                "**सीएसएमटी**: यूनेस्को विरासत रेलवे स्टेशन की विक्टोरियन गॉथिक वास्तुकला की प्रशंसा करें।",
                "**मणि भवन**: महात्मा गांधी के पूर्व निवास का दौरा करें, जो अब ऐतिहासिक पत्रों वाला एक संग्रहालय है।",
                "**गेटवे ऑफ इंडिया**: राजा जॉर्ज पंचम की यात्रा की याद में निर्मित भव्य स्मारक को देखें।",
                "**कान्हरी गुफाएं**: राष्ट्रीय उद्यान के भीतर स्थित बौद्ध धर्म की प्राचीन गुफाओं का अन्वेषण करें।",
                "**वसई किला**: तटीय क्षेत्र में स्थित पुर्तगाली किले के विशाल खंडहरों को देखने के लिए एक दिवसीय यात्रा करें।",
                "**हाजी अली दरगाह**: वर्ली के तट पर एक छोटे द्वीप पर स्थित 15वीं शताब्दी की मस्जिद के दर्शन करें।",
                "**भाऊ दाजी लाड संग्रहालय**: मुंबई के सबसे पुराने संग्रहालय का भ्रमण करें, जिसमें मिट्टी के मॉडल प्रदर्शित हैं।"
            ],
            "te": [
                "**ఎలిఫెంటా గుహలు**: సముద్రంలో పడవ ప్రయాణం చేస్తూ కొండలను తొలిచి నిర్మించిన పురాతన శిల్పకళా గుహలను సందర్శించండి.",
                "**CSMT**: విక్టోరియన్ గోతిక్ నిర్మాణ శైలి కలిగిన యునెస్కో గుర్తింపు పొందిన రైల్వే స్టేషన్ భవనాన్ని తిలకించండి.",
                "**మణి భవన్**: గాంధీజీ ముంబైలో నివసించిన గృహాన్ని (ప్రస్తుతం మ్యూజియం) సందర్శించండి.",
                "**గేట్‌వే ఆఫ్ ఇండియా**: బ్రిటీష్ రాజు జార్జ్ V రాకకు జ్ఞాపికగా నిర్మించిన ముంబై ప్రధాన చిహ్నాన్ని సందర్శించండి.",
                "**కన్హేరి గుహలు**: సంజయ్ గాంధీ పార్క్ లోపల కొండల్లో తొలిచిన పురాతన బౌద్ధ గుహలను సందర్శించండి.",
                "**వసాయ్ కోట**: పోర్చుగీస్ కాలం నాటి పురాతన కోట శిథిలాలను సందర్శించడానికి వసాయ్ కి విహారయాత్ర చేయండి.",
                "**హాజీ అలీ దర్గా**: సముద్రం మధ్యలో ఒక చిన్న రాతి తిన్నె పై నిర్మించబడిన చారిత్రక దర్గాను సందర్శించండి.",
                "**భావూ దాజీ లాడ్ మ్యూజియం**: ముంబై చరిత్రను ప్రతిబింబించే మట్టి బొమ్మలు గల పురాతన మ్యూజియాన్ని సందర్శించండి."
            ]
        },
        "default": {
            "en": [
                "**Gateway of India**: Visit this iconic landmark built in the early 20th century.",
                "**Marine Drive**: Take a stroll along the Queen's Necklace promenade.",
                "**Street Food**: Try authentic Vada Pav near local railway stations or beach fronts.",
                "**Haji Ali Dargah**: Walk along the narrow causeway to the floating tomb during low tide.",
                "**Elephanta Caves**: Take a morning ferry from Apollo Bunder to explore the island caves.",
                "**Colaba Causeway**: Browse the street bazaar for handicrafts and souvenir items.",
                "**Sea Link & Bandra**: Drive across the spectacular Bandra-Worli Sea Link and explore Bandra Fort.",
                "**Juhu Beach**: Spend an evening walking on the sand and savoring local Pav Bhaji."
            ],
            "hi": [
                "**गेटवे ऑफ इंडिया**: 20वीं सदी की शुरुआत में निर्मित इस ऐतिहासिक स्मारक के दर्शन करें।",
                "**मरीन ड्राइव**: क्वींस नेकलेस के नाम से प्रसिद्ध सैरगाह पर शाम को टहलें।",
                "**स्ट्रीट फूड**: स्थानीय रेलवे स्टेशनों या समुद्र तट के पास प्रामाणिक वड़ा पाव का स्वाद लें।",
                "**हाजी अली दरगाह**: कम ज्वार के दौरान तैरती हुई दरगाह तक जाने वाले संकीर्ण मार्ग पर टहलें।",
                "**एलीफेंटा की गुफाएं**: द्वीप गुफाओं का अन्वेषण करने के लिए अपोलो बंदर से सुबह की नौका लें।",
                "**कोलाबा कॉजवे**: हस्तशिल्प और स्मृति चिन्हों के लिए स्ट्रीट बाजार का भ्रमण करें।",
                "**सी लिंक और बांद्रा**: शानदार बांद्रा-वर्ली सी लिंक से गुजरें और बांद्रा किले का दौरा करें।",
                "**जुहू बीच**: शाम को रेत पर टहलने और स्थानीय पाव भाजी का स्वाद लेने में समय बिताएं।"
            ],
            "te": [
                "**గేట్‌వే ఆఫ్ ఇండియా**: 20వ శతాబ్దపు ప్రారంభంలో నిర్మించబడిన ముంబై ఐకానిక్ ల్యాండ్‌మార్క్‌ను సందర్శించండి.",
                "**మెరైన్ డ్రైవ్**: రాణి హారంగా పిలవబడే సముద్ర తీర మార్గం వెంబడి సాయంత్రం నడకను ఆస్వాదించండి.",
                "**వీధి ఆహారాలు**: ముంబై రైల్వే స్టేషన్ల సమీపంలో లభించే వేడి వేడి వడా పావ్ ని రుచి చూడండి.",
                "**హాజీ అలీ దర్గా**: అలలు తక్కువగా ఉన్న సమయంలో సముద్ర మార్గం గుండా వెళ్లి దర్గాను సందర్శించండి.",
                "**ఎలిఫెంటా గుహలు**: అపోలో బందర్ నుండి ఉదయమే పడవ ప్రయాణం చేసి గుహలను సందర్శించండి.",
                "**కోలాబా కాజ్‌వే**: బజార్లలో లభించే హస్తకళల వస్తువులను మరియు బహుమతులను కొనుగోలు చేయండి.",
                "**సీ లింక్ & బాంద్రా**: అద్భుతమైన బాంద్రా-వర్లీ వంతెన గుండా ప్రయాణించి బాంద్రా కోటను సందర్శించండి.",
                "**జుహూ బీచ్**: సాయంత్రం బీచ్ ఇసుకలో విహరిస్తూ స్థానిక పావ్ భాజీని ఆస్వాదించండి."
            ]
        }
    },
    "kolkata": {
        "temples": {
            "en": [
                "**Dakshineswar Kali**: Visit the famous 19th-century temple on the banks of Hooghly River.",
                "**Kalighat**: Explore the ancient temple, one of the 51 Shakti Peethas, dedicated to Goddess Kali.",
                "**Belur Math**: Visit the tranquil headquarters of Ramakrishna Mission, representing architecture of all religions.",
                "**Birla Temple**: Visit the grand white marble temple displaying fine carvings in South Kolkata.",
                "**St. Paul's Cathedral**: Admire the Indo-Gothic style architecture of the majestic cathedral.",
                "**Pareshnath Jain Temple**: Explore the stunning mirror-decorated temple complex, surrounded by gardens.",
                "**Chinese Kali Temple**: Visit the unique temple in Tangra where noodles are offered as prasad.",
                "**Lake Kalibari**: Spend a quiet evening at the serene temple dedicated to Goddess Kali near Southern Avenue."
            ],
            "hi": [
                "**दक्षिणेश्वर काली**: हुगली नदी के तट पर स्थित प्रसिद्ध 19वीं सदी के मंदिर के दर्शन करें।",
                "**कालीघाट**: देवी काली को समर्पित प्राचीन मंदिर के दर्शन करें, जो 51 शक्ति पीठों में से एक है।",
                "**बेलूर मठ**: रामकृष्ण मिशन के शांत मुख्यालय का दौरा करें, जो सभी धर्मों की वास्तुकला का प्रतिनिधित्व करता है।",
                "**बिड़ला मंदिर**: दक्षिण कोलकाता में बेहतरीन नक्काशी प्रदर्शित करने वाले भव्य सफेद संगमरमर के मंदिर के दर्शन करें।",
                "**सेंट पॉल कैथेड्रल**: भव्य कैथेड्रल की इंडो-गोथिक शैली की वास्तुकला की प्रशंसा करें।",
                "**पारसनाथ जैन मंदिर**: बगीचों से घिरे, शीशों से सजे सुंदर मंदिर परिसर का अन्वेषण करें।",
                "**चाइनीज काली मंदिर**: टांगरा में स्थित अनोखे मंदिर के दर्शन करें जहां नूडल्स को प्रसाद के रूप में चढ़ाया जाता है।",
                "**लेक कालीबाड़ी**: साउदर्न एवेन्यू के पास देवी काली को समर्पित शांत मंदिर में एक शांतिपूर्ण शाम बिताएं।"
            ],
            "te": [
                "**దక్షిణేశ్వర్ కాళీ ఆలయం**: హుగ్లీ నది ఒడ్డున ఉన్న ప్రసిద్ధ 19వ శతాబ్దపు కాళీ ఆలయాన్ని సందర్శించండి.",
                "**కాళీఘాట్ ఆలయం**: 51 శక్తి పీఠాలలో ఒకటైన పురాతన కాళీఘాట్ కాళీ ఆలయాన్ని సందర్శించండి.",
                "**బేలూరు మఠం**: అన్ని మతాల సమ్మేళన నిర్మాణ శైలితో కూడిన రామకృష్ణ మిషన్ ప్రధాన కార్యాలయాన్ని సందర్శించండి.",
                "**బిర్లా మందిరం**: దక్షిణ కోల్‌కతాలో అద్భుత శిల్పకళతో అలరారే తెల్లటి పాలరాతి ఆలయాన్ని సందర్శించండి.",
                "**సెయింట్ పాల్స్ కాథెడ్రల్**: ఇండో-గోతిక్ శైలిలో నిర్మించబడిన సుందరమైన చర్చిని సందర్శించండి.",
                "**పరేష్‌నాథ్ జైన్ ఆలయం**: రంగురంగుల అద్దాలతో మరియు అందమైన తోటలతో అలంకరించబడిన జైన్ ఆలయాన్ని అన్వేషించండి.",
                "**చైనీస్ కాళీ ఆలయం**: టాంగ్రాలోని చారిత్రక ఆలయం, ఇక్కడ నూడిల్స్ ని ప్రసాదంగా సమర్పిస్తారు.",
                "**లేక్ కాళీబారి**: సదరన్ అవెన్యూ సమీపంలోని ప్రశాంతమైన కాళీ ఆలయాన్ని సందర్శించి ప్రశాంతతను పొందండి."
            ]
        },
        "food": {
            "en": [
                "**Kathi Rolls**: Try the legendary street-style Kathi Rolls at Nizam's or Kusum Rolls on Park Street.",
                "**Fish Curry**: Savor an authentic Bengali fish curry (Maachher Jhol) and rice meal at a traditional diner.",
                "**Sweets**: Taste world-famous Rasgulla, Sandesh, and sweet yogurt (Mishti Doi) at legendary confectioneries.",
                "**Phuchka**: Try the spicy water-filled potato dumplings near Vivekananda Park street stalls.",
                "**Mughlai Paratha**: Relish the deep-fried egg-filled flatbread at historic Anadi Cabin.",
                "**Mitra Cafe**: Sample traditional Bengali snacks like fish fry, cutlets, and brain chops.",
                "**Telebhaja**: Try hot onion, potato, and eggplant fritters from street corners like Kalika.",
                "**Tangra Chinese**: Visit Kolkata's Chinatown to savor authentic Indian-Chinese cuisine."
            ],
            "hi": [
                "**काठी रोल**: पार्क स्ट्रीट पर निज़ाम या कुसुम रोल्स में प्रसिद्ध काठी रोल का स्वाद लें।",
                "**फिश करी**: एक पारंपरिक रेस्तरां में प्रामाणिक बंगाली मछली करी (माछेर झोल) और चावल का आनंद लें।",
                "**मिठाइयाँ**: ऐतिहासिक हलवाइयों की दुकानों पर विश्व प्रसिद्ध रसगुल्ला, संदेश और मिष्टी दोई का स्वाद लें।",
                "**पुचका**: विवेकानंद पार्क के पास स्थित स्ट्रीट स्टालों पर तीखे पानी से भरे पुचके का स्वाद लें।",
                "**मुगलई पराठा**: ऐतिहासिक अनादि केबिन में तले हुए अंडे से भरे पराठे का स्वाद लें।",
                "**मित्रा कैफे**: फिश फ्राई, कटलेट और चॉप्स जैसे पारंपरिक बंगाली स्नैक्स का आनंद लें।",
                "**टेलीभाजा**: कालिका जैसी दुकानों से गरमा-गरम प्याज, आलू और बैंगन के पकोड़ों का स्वाद लें।",
                "**टांगरा चाइनीज**: प्रामाणिक भारतीय-चीनी व्यंजनों का स्वाद लेने के लिए कोलकाता के चाइनाटाउन का दौरा करें।"
            ],
            "te": [
                "**కాఠీ రోల్స్**: పార్క్ స్ట్రీట్ లోని నిజామ్ లేదా కుసుమ్ రోల్స్ వద్ద లభించే రుచికరమైన కాఠీ రోల్స్ ని ప్రయత్నించండి.",
                "**చేపల పులుసు**: సాంప్రదాయ రెస్టారెంట్‌లో బెంగాలీ చేపల పులుసు (చేపల కూర) మరియు అన్నం రుచి చూడండి.",
                "**బెంగాలీ స్వీట్లు**: ఇక్కడి ప్రసిద్ధ రసగుల్లా, సందేష్ మరియు తీపి పెరుగు (మిష్టీ దోయి)లను రుచి చూడండి.",
                "**పుచ్కా**: వివేకానంద పార్క్ వద్ద లభించే కారంగా ఉండే పుచ్కా (పానీపూరి)ని ప్రయత్నించండి.",
                "**మొఘలాయ్ పరాటా**: అనాది క్యాబిన్ వద్ద లభించే గుడ్డు మిశ్రమంతో కూడిన మొఘలాయ్ పరాటాను ఆస్వాదించండి.",
                "**మిత్రా కేఫ్**: ఇక్కడి సాంప్రదాయ బెంగాలీ స్నాక్స్ అయిన ఫిష్ ఫ్రై మరియు కట్లెట్లను రుచి చూడండి.",
                "**టెలిభాజా**: రోడ్డు పక్కన లభించే ఉల్లిపాయ, ఆలుగడ్డ మరియు వంకాయ బజ్జీలను ఆస్వాదించండి.",
                "**టాంగ్రా చైనీస్**: కోల్‌కతా చైనాటౌన్ లో లభించే ప్రామాణికమైన ఇండో-చైనీస్ వంటకాలను ప్రయత్నించండి."
            ]
        },
        "nature": {
            "en": [
                "**Botanical Garden**: See the historic Great Banyan Tree, one of the largest trees in the world.",
                "**Eco Park**: Visit the massive ecological park in New Town featuring replicas of wonders and boating.",
                "**Rabindra Sarobar**: Take a peaceful morning walk along the clean lake, surrounded by greenery.",
                "**Maidan**: Relax on the vast green open lawns, the lung space in the center of Kolkata.",
                "**Subhash Sarobar**: Walk around the beautiful lake in East Kolkata, popular for bird watching.",
                "**Central Park**: Explore the beautiful park in Salt Lake City, featuring flower beds and water streams.",
                "**Bird Sanctuary**: Visit the Chintamoni Kar Bird Sanctuary to spot local butterfly and bird species.",
                "**Millennium Park**: Stroll in the landscaped park along the Hooghly River bank, viewing the bridge."
            ],
            "hi": [
                "**वानस्पतिक उद्यान**: ऐतिहासिक ग्रेट बरगद का पेड़ देखें, जो दुनिया के सबसे बड़े पेड़ों में से एक है।",
                "**इको पार्क**: न्यू टाउन में स्थित विशाल पारिस्थितिकी पार्क का दौरा करें, जहां अजूबों की प्रतिकृतियां और नौका विहार की सुविधा है।",
                "**रवींद्र सरोवर**: हरियाली से घिरी इस साफ झील के किनारे सुबह की शांतिपूर्ण सैर करें।",
                "**मैदान**: कोलकाता के केंद्र में स्थित विशाल हरे-भरे मैदानों में आराम करें, जो शहर का फेफड़ा है।",
                "**सुभाष सरोवर**: पूर्वी कोलकाता में स्थित सुंदर झील के चारों ओर टहलें, जो पक्षियों को देखने के लिए प्रसिद्ध है।",
                "**सेंट्रल पार्क**: साल्ट लेक सिटी में फूलों की क्यारियों और जलधाराओं वाले सुंदर पार्क का अन्वेषण करें।",
                "**पक्षी अभयारण्य**: स्थानीय तितलियों और पक्षियों की प्रजातियों को देखने के लिए चिंतामणि कर पक्षी अभयारण्य का दौरा करें।",
                "**मिलेनियम पार्क**: हुगली नदी के तट पर बने सुंदर पार्क में टहलें और हुगली ब्रिज का दृश्य देखें।"
            ],
            "te": [
                "**బొటానికల్ గార్డెన్**: ప్రపంచంలోనే అతిపెద్ద చెట్లలో ఒకటైన చారిత్రక 'మహా మర్రి వృక్షం' (గ్రేట్ బన్యన్ ట్రీ)ను సందర్శించండి.",
                "**ఎకో పార్క్**: న్యూ టౌన్ లోని భారీ పార్కును సందర్శించి అందులోని వింతల నమూనాలను మరియు బోటింగ్ ను ఆస్వాదించండి.",
                "**రవీంద్ర సరోవర్**: పచ్చదనంతో నిండిన సరస్సు వెంబడి ప్రశాంతమైన ఉదయపు నడకను ఆస్వాదించండి.",
                "**మైదాన్**: కోల్‌కతా నడిబొడ్డున ఉండే విశాలమైన పచ్చని మైదానాలలో విశ్రాంతి తీసుకోండి.",
                "**సుభాష్ సరోవర్**: తూర్పు కోల్‌కతాలోని పక్షుల వీక్షణకు అనువైన అందమైన సరస్సు చుట్టూ నడవండి.",
                "**సెంట్రల్ పార్క్**: సాల్ట్ లేక్ లోని పూల తోటలు మరియు కాలువలతో కూడిన అందమైన పార్కును అన్వేషించండి.",
                "**చింతామణి కర్ పక్షుల కేంద్రం**: వివిధ రకాల పక్షులు మరియు సీతాకోకచిలుకలు గల సంరక్షణ కేంద్రాన్ని సందర్శించండి.",
                "**మిలీనియం పార్క్**: హుగ్లీ నది ఒడ్డున గల పార్కులో నడుస్తూ నది మరియు వంతెనల అందాలను వీక్షించండి."
            ]
        },
        "shopping": {
            "en": [
                "**New Market**: Shop for silver jewelry, sarees, garments, and traditional cheese in the historic complex.",
                "**Gariahat**: Browse the endless rows of stalls for traditional Tant and Korial silk sarees.",
                "**College Street**: Explore the world's largest second-hand book market and historic publishing houses.",
                "**Dakshinapan**: Buy authentic Indian handicrafts and handloom fabrics from government emporiums.",
                "**Hatibagan**: Browse the bustling market in North Kolkata for budget clothes and accessories.",
                "**Burrabazar**: Experience the high-energy wholesale market selling fabrics, toys, and wedding items.",
                "**Kumartuli**: Visit the unique potters' colony to see artisans carving clay idols of Durga.",
                "**Quest Mall**: Shop for premium international brands and visit boutique designers."
            ],
            "hi": [
                "**न्यू मार्केट**: ऐतिहासिक बाजार परिसर में चांदी के गहनों, साड़ियों, कपड़ों और पारंपरिक पनीर की खरीदारी करें।",
                "**गरियाहाट**: पारंपरिक तांत और कोरियाल रेशमी साड़ियों के लिए दुकानों की अंतहीन कतारें देखें।",
                "**कॉलेज स्ट्रीट**: दुनिया के सबसे बड़े सेकेंड-हैंड बुक मार्केट और ऐतिहासिक प्रकाशन गृहों का अन्वेषण करें।",
                "**दक्षिणापन**: सरकारी एम्पोरियम से प्रामाणिक भारतीय हस्तशिल्प और हथकरघा कपड़े खरीदें।",
                "**हातीबागान**: उत्तर कोलकाता के हलचल भरे बाजार में बजट के अनुकूल कपड़े और सामान की खरीदारी करें।",
                "**बड़ाबाजार**: कपड़े, खिलौने और शादी के सामान बेचने वाले ऊर्जावान थोक बाजार का अनुभव करें।",
                "**कुम्हारटोली**: मिट्टी की दुर्गा मूर्तियां बनाने वाले कारीगरों को देखने के लिए कुम्हार कॉलोनी का दौरा करें।",
                "**क्वेस्ट मॉल**: प्रीमियम अंतर्राष्ट्रीय ब्रांडों और बुटीक डिजाइनरों की खरीदारी करें।"
            ],
            "te": [
                "**న్యూ మార్కెట్**: ఈ చారిత్రక మార్కెట్ సముదాయంలో వెండి ఆభరణాలు, చీరలు మరియు సాంప్రదాయ వస్తువులను కొనుగోలు చేయండి.",
                "**గరియాహట్**: బెంగాలీ సాంప్రదాయ కాటన్ మరియు సిల్క్ చీరల కోసం ఇక్కడి దుకాణాలను సందర్శించండి.",
                "**కాలేజ్ స్ట్రీట్**: ప్రపంచంలోనే అతిపెద్ద సెకండ్ హ్యాండ్ పుస్తకాల మార్కెట్ ను సందర్శించి పుస్తకాలను సేకరించండి.",
                "**దక్షిణాపన్**: వివిధ రాష్ట్రాల ప్రభుత్వ హస్తకళల కేంద్రాల నుండి నాణ్యమైన వస్తువులను కొనుగోలు చేయండి.",
                "**హతీబగాన్**: ఉత్తర కోల్‌కతాలోని బడ్జెట్ ధరలలో లభించే దుస్తుల మార్కెట్ ను సందర్శించండి.",
                "**బారాబజార్**: దుస్తులు, బొమ్మలు మరియు పెళ్లి సామాగ్రి దొరికే అత్యంత రద్దీ గల హోల్‌సేల్ మార్కెట్‌ను అనుభవించండి.",
                "**కుమార్తులి**: దేవీ దుర్గ మట్టి విగ్రహాలను తయారు చేసే చారిత్రక కుమ్మరి కాలనీని సందర్శించండి.",
                "**క్వెస్ట్ మాల్**: ఆధునిక అంతర్జాతీయ బ్రాండ్లు మరియు ఫ్యాషన్ వస్తువుల షాపింగ్ కోసం ఇక్కడికి వెళ్ళండి."
            ]
        },
        "history": {
            "en": [
                "**Indian Museum**: Explore the oldest and largest museum in India, showcasing fossils and art.",
                "**Marble Palace**: Tour the private 19th-century mansion featuring marble sculptures and paintings.",
                "**Jorasanko Thakur Bari**: Visit the ancestral home of Rabindranath Tagore, now a museum.",
                "**Victoria Memorial**: Admire the grand white marble monument built to commemorate Queen Victoria.",
                "**Howrah Bridge**: View the engineering marvel, a cantilever bridge crossing the Hooghly River.",
                "**Writer's Building**: Admire the historical Greco-Roman style architecture of the administrative seat.",
                "**Fort William**: Tour the historic British fort located on the eastern banks of Hooghly River.",
                "**Netaji Bhawan**: Visit Netaji Subhas Chandra Bose's ancestral home, preserved as a historical museum."
            ],
            "hi": [
                "**भारतीय संग्रहालय**: भारत के सबसे पुराने और सबसे बड़े संग्रहालय का अन्वेषण करें, जिसमें जीवाश्म और कला प्रदर्शित हैं।",
                "**मार्बल पैलेस**: संगमरमर की मूर्तियों और चित्रों से सजी 19वीं सदी की निजी हवेली का दौरा करें।",
                "**जोरासांको ठाकुर बाड़ी**: रवींद्रनाथ टैगोर के पैतृक घर का दौरा करें, जो अब एक संग्रहालय है।",
                "**विक्टोरिया मेमोरियल**: रानी विक्टोरिया की याद में निर्मित भव्य सफेद संगमरमर के स्मारक की वास्तुकला को देखें।",
                "**हावड़ा ब्रिज**: हुगली नदी पर बने कैंटिलीवर ब्रिज की भव्य इंजीनियरिंग कला को देखें।",
                "**राइटर्स बिल्डिंग**: प्रशासनिक कार्यालय के ऐतिहासिक ग्रीको-रोमन शैली के स्थापत्य सौंदर्य की प्रशंसा करें।",
                "**फोर्ट विलियम**: हुगली नदी के पूर्वी तट पर स्थित ऐतिहासिक ब्रिटिश किले का दौरा करें।",
                "**नेताजी भवन**: नेताजी सुभाष चंद्र बोस के पैतृक घर का दौरा करें, जिसे ऐतिहासिक संग्रहालय के रूप में संरक्षित किया गया है।"
            ],
            "te": [
                "**ఇండియన్ మ్యూజియం**: భారతదేశంలోనే అత్యంత పురాతనమైన మరియు అతిపెద్ద మ్యూజియంను సందర్శించి అద్భుత కళాఖండాలను వీక్షించండి.",
                "**మార్బుల్ ప్యాలెస్**: పాలరాతి శిల్పాలు మరియు పెయింటింగ్స్ గల 19వ శతాబ్దపు రాజప్రసాదాన్ని సందర్శించండి.",
                "**జోరాశాంకో ఠాకూర్ బారి**: రవీంద్రనాథ్ ఠాగూర్ పూర్వీకుల నివాసాన్ని (ప్రస్తుతం మ్యూజియం) సందర్శించండి.",
                "**విక్టోరియా మెమోరియల్**: తెల్లటి పాలరాతితో విక్టోరియా రాణి జ్ఞాపికగా నిర్మించిన అద్భుత కట్టడాన్ని సందర్శించండి.",
                "**హౌరా బ్రిడ్జి**: హుగ్లీ నదిపై ఎలాంటి ఆధార స్తంభాలు లేకుండా కట్టిన చారిత్రక హౌరా వంతెనను వీక్షించండి.",
                "**రైటర్స్ బిల్డింగ్**: గ్రీకో-రోమన్ శైలిలో నిర్మించబడిన చారిత్రక పరిపాలన భవనాన్ని తిలకించండి.",
                "**ఫోర్ట్ విలియం**: హుగ్లీ నది ఒడ్డున బ్రిటిష్ కాలంలో నిర్మించబడిన చారిత్రక కోటను సందర్శించండి.",
                "**నేతాజీ భవన్**: నేతాజీ సుభాష్ చంద్రబోస్ నివసించిన గృహాన్ని సందర్శించి చారిత్రక వస్తువులను గమనించండి."
            ]
        },
        "default": {
            "en": [
                "**Victoria Memorial**: Explore the grand marble building built during the British rule.",
                "**Howrah Bridge**: Walk or drive across the iconic bridge over the Hooghly River.",
                "**Sweets**: Try traditional sweets like Rasgulla and Mishti Doi from local sweet shops.",
                "**Dakshineswar Kali**: Visit the grand temple and watch the ferry boats on the river.",
                "**Belur Math**: Explore the calm monastery and sit by the peaceful river bank.",
                "**Park Street**: Enjoy dining at classic English tea rooms and heritage restaurants.",
                "**College Street**: Stroll through the historic book lane and visit the Indian Coffee House.",
                "**Princep Ghat**: Enjoy an evening walk along the river bank and watch the illuminated Vidyasagar Setu."
            ],
            "hi": [
                "**विक्टोरिया मेमोरियल**: ब्रिटिश शासन के दौरान बनी भव्य संगमरमर की इमारत का अन्वेषण करें।",
                "**हावड़ा ब्रिज**: हुगली नदी पर बने इस प्रतिष्ठित पुल पर चलें या ड्राइव करें।",
                "**मिठाइयाँ**: स्थानीय दुकानों से रसगुल्ला और मिष्टी दोई जैसी पारंपरिक मिठाइयों का आनंद लें।",
                "**दक्षिणेश्वर काली**: भव्य मंदिर के दर्शन करें और नदी में नावों को चलते हुए देखें।",
                "**बेलूर मठ**: शांत मठ का अन्वेषण करें और नदी के किनारे शांति से बैठें।",
                "**पार्क स्ट्रीट**: क्लासिक चाय घरों और विरासत रेस्तरां में भोजन का आनंद लें।",
                "**कॉलेज स्ट्रीट**: ऐतिहासिक पुस्तक लेन में घूमें और इंडियन कॉफी हाउस का दौरा करें।",
                "**प्रिंसेप घाट**: नदी के किनारे शाम की सैर का आनंद लें और रोशनी से जगमगाते विद्यासागर सेतु को देखें।"
            ],
            "te": [
                "**విక్టోరియా మెమోరియల్**: బ్రిటిష్ కాలం నాటి అద్భుతమైన తెల్లటి పాలరాతి భవనాన్ని సందర్శించండి.",
                "**హౌరా బ్రిడ్జి**: హుగ్లీ నదిపై ఉన్న ఐకానిక్ హౌరా వంతెన గుండా ప్రయాణాన్ని అనుభవించండి.",
                "**బెంగాలీ మిఠాయిలు**: స్థానిక దుకాణాలలో లభించే సాంప్రదాయ రసగుల్లా మరియు మిష్టీ దోయిలను ఆస్వాదించండి.",
                "**దక్షిణేశ్వర్ కాళీ**: ప్రసిద్ధ కాళీ ఆలయాన్ని దర్శించి నదిలోని పడవల ప్రయాణాన్ని గమనించండి.",
                "**బేలూరు మఠం**: ప్రశాంతమైన రామకృష్ణ మఠాన్ని సందర్శించి నదీ తీరంలో సమయం గడపండి.",
                "**పార్క్ స్ట్రీట్**: ఇక్కడి చారిత్రక రెస్టారెంట్లలో సాంప్రదాయ వంటకాలను ఆస్వాదించండి.",
                "**కాలేజ్ స్ట్రీట్**: పుస్తకాల బజార్లలో విహరించి ప్రసిద్ధ ఇండియన్ కాఫీ హౌస్ ను సందర్శించండి.",
                "**ప్రిన్సెప్ ఘాట్**: సాయంత్రం వేళ నదీ తీరంలో విహరిస్తూ విద్యుత్ కాంతులతో వెలిగిపోయే విద్యాసాగర్ సేతును తిలకించండి."
            ]
        }
    },
    "delhi": {
        "temples": {
            "en": [
                "**Akshardham**: Visit the massive modern temple showcasing stone carvings and water show.",
                "**Lotus Temple**: Explore the flower-shaped Bahai House of Worship, a place of silent prayer.",
                "**Jama Masjid**: Visit the grand historical mosque built of red sandstone in Old Delhi.",
                "**Gurudwara Bangla Sahib**: Visit the famous Sikh temple known for its golden dome and community kitchen.",
                "**Birla Mandir**: Explore the colorful Laxminarayan Temple dedicated to Lord Vishnu and Laxmi.",
                "**Chhattarpur Temple**: Visit the massive temple complex built in South Indian architecture style.",
                "**Kalkaji Mandir**: Visit the ancient temple dedicated to Goddess Kali, hosting thousands of devotees.",
                "**Nizamuddin Dargah**: Attend the soulful evening Sufi Qawwali performances at the historical mausoleum."
            ],
            "hi": [
                "**अक्षरधाम**: पत्थर की नक्काशी और जल शो प्रदर्शित करने वाले विशाल आधुनिक मंदिर के दर्शन करें।",
                "**लोटस टेम्पल**: शांत प्रार्थना के स्थान, कमल के आकार के बहाई उपासना गृह का अन्वेषण करें।",
                "**जामा मस्जिद**: पुरानी दिल्ली में लाल बलुआ पत्थर से बनी भव्य ऐतिहासिक मस्जिद के दर्शन करें।",
                "**गुरुद्वारा बंगला साहिब**: अपने सुनहरे गुंबद और लंगर (सामुदायिक रसोई) के लिए प्रसिद्ध सिख गुरुद्वारे के दर्शन करें।",
                "**बिड़ला मंदिर**: भगवान विष्णु और लक्ष्मी को समर्पित रंगीन लक्ष्मीनारायण मंदिर का अन्वेषण करें।",
                "**छतरपुर मंदिर**: दक्षिण भारतीय वास्तुकला शैली में निर्मित विशाल मंदिर परिसर के दर्शन करें।",
                "**कालकाजी मंदिर**: देवी काली को समर्पित प्राचीन मंदिर के दर्शन करें, जहां हजारों भक्त आते हैं।",
                "**निजामुद्दीन दरगाह**: ऐतिहासिक दरगाह पर शाम को होने वाले रूहानी सूफी कव्वाली कार्यक्रमों में भाग लें।"
            ],
            "te": [
                "**అక్షరధామ్ ఆలయం**: అద్భుతమైన రాతి శిల్పాలు మరియు వాటర్ షో కలిగిన భారీ ఆధునిక ఆలయాన్ని సందర్శించండి.",
                "**లోటస్ టెంపుల్**: ప్రశాంతమైన ధ్యానానికి అనువైన, కమలం ఆకృతిలో నిర్మించిన బహాయి ప్రార్థనా మందిరాన్ని సందర్శించండి.",
                "**జామా మసీదు**: పాత ఢిల్లీలోని ఎర్రరాయితో నిర్మించబడిన భారతదేశపు అతిపెద్ద చారిత్రక మసీదును సందర్శించండి.",
                "**గురుద్వారా బంగ్లా సాహిబ్**: బంగారు గోపురం మరియు ఉచిత లంగర్ (భోజన సదుపాయం) గల ప్రసిద్ధ సిక్కు దేవాలయాన్ని సందర్శించండి.",
                "**బిర్లా మందిరం**: విష్ణుమూర్తి మరియు లక్ష్మీ దేవిలకు అంకితం చేయబడిన రంగురంగుల లక్ష్మీనారాయణ ఆలయాన్ని సందర్శించండి.",
                "**ఛతర్‌పూర్ ఆలయం**: దక్షిణ భారత నిర్మాణ శైలిలో నిర్మించబడిన అతిపెద్ద దేవాలయ సముదాయాన్ని సందర్శించండి.",
                "**కల్కాజీ ఆలయం**: కాళీ దేవికి అంకితం చేయబడిన పురాతన కల్కాజీ ఆలయాన్ని దర్శించండి.",
                "**నిజాముద్దీన్ దర్గా**: ఇక్కడి దర్గాలో సాయంత్రం జరిగే ఆధ్యాత్మిక సూఫీ ఖవ్వాలీ గానాన్ని వినడానికి వెళ్ళండి."
            ]
        },
        "food": {
            "en": [
                "**Paranthe Wali Gali**: Eat unique deep-fried stuffed flatbreads in the narrow streets of Chandni Chowk.",
                "**Jama Masjid Area**: Try Mughlai food, seekh kebabs, and chicken tikka in Old Delhi.",
                "**Connaught Place**: Enjoy global dining and cafe crawl in the historic British colonnaded hub.",
                "**Sitaram Chole Bhature**: Savor Delhi's most famous spicy chole and paneer-stuffed bhature.",
                "**UPSC Lane Chaat**: Try spicy local street food, aloo tikki, and gol gappe at legendary stalls.",
                "**Majnu ka Tilla**: Visit the Tibetan colony for authentic momos, laphing, and butter tea.",
                "**Kuremal Kulfi**: Sample unique fruit-stuffed kulfis at the legendary shop in Old Delhi.",
                "**Lajpat Nagar**: Savor delicious street snacks, ram ladoo (lentil dumplings), and chaat."
            ],
            "hi": [
                "**पराठे वाली गली**: चांदनी चौक की संकरी गलियों में अनोखे तले हुए भरवां पराठों का स्वाद लें।",
                "**जामा मस्जिद क्षेत्र**: पुरानी दिल्ली में मुगलई भोजन, सीख कवाब और चिकन टिक्का का स्वाद लें।",
                "**कनॉट प्लेस**: ऐतिहासिक ब्रिटिश औपनिवेशिक वास्तुकला वाले केंद्र में वैश्विक भोजन और कैफे संस्कृति का आनंद लें।",
                "**सीताराम छोले भटूरे**: दिल्ली के सबसे प्रसिद्ध मसालेदार छोले और पनीर से भरे भटूरों का स्वाद लें।",
                "**यूपीएससी लेन चाट**: प्रसिद्ध स्टालों पर तीखा स्थानीय स्ट्रीट फूड, आलू टिक्की और गोलगप्पे खाएं।",
                "**मजनू का टीला**: तिब्बती बस्ती में प्रामाणिक मोमोज, लाफिंग और बटर टी का स्वाद लें।",
                "**कुरेमल कुल्फी**: पुरानी दिल्ली की ऐतिहासिक दुकान पर फलों से भरी अनोखी कुल्फी का स्वाद लें।",
                "**लाजपत नगर**: स्वादिष्ट स्ट्रीट स्नैक्स, राम लड्डू (दाल के पकोड़े) और चाट का आनंद लें।"
            ],
            "te": [
                "**పరాఠేవాలీ గల్లీ**: చాందినీ చౌక్ వీధుల్లో లభించే వివిధ రకాల వేయించిన పరాఠాలను రుచి చూడండి.",
                "**జామా మసీదు ప్రాంతం**: పాత ఢిల్లీలో లభించే మొఘలాయ్ బిర్యానీ మరియు వివిధ రకాల కబాబ్స్ ని ప్రయత్నించండి.",
                "**కన్నాట్ ప్లేస్**: బ్రిటిష్ కాలం నాటి కట్టడాలు గల కన్నాట్ ప్లేస్ లో ఆధునిక భోజనం మరియు కాఫీలను ఆస్వాదించండి.",
                "**సీతారామ్ చోలే బటూరే**: ఢిల్లీలో అత్యంత ప్రసిద్ధి చెందిన మసాలా చోలే బటూరేలను రుచి చూడండి.",
                "**UPSC లేన్ చాట్**: ఇక్కడి ప్రసిద్ధ స్టాల్స్ వద్ద ఆలు టిక్కీ, పానీపూరి వంటి చాట్ ఐటమ్స్ ప్రయత్నించండి.",
                "**మజ్ను కా తిల్లా**: టిబెటన్ కాలనీలో లభించే మోమోస్, లాఫింగ్ మరియు బటర్ టీలను ఆస్వాదించండి.",
                "**కురేమల్ కుల్ఫీ**: పాత ఢిల్లీలోని పురాతన షాపులో పండ్ల ముక్కలతో నిండిన కుల్ఫీని రుచి చూడండి.",
                "**లాజ్‌పత్ నగర్**: ఇక్కడి వీధుల్లో లభించే రుచికరమైన రామ్ లడ్డూలు మరియు చాట్ లను ఆస్వాదించండి."
            ]
        },
        "nature": {
            "en": [
                "**Lodhi Gardens**: Walk amidst green lawns housing grand 15th-century historical tombs.",
                "**Sunder Nursery**: Explore the beautifully restored Mughal-era heritage park and plant nursery.",
                "**Garden of Five Senses**: Relax in the scenic thematic garden featuring fountains and sculptures.",
                "**Yamuna Biodiversity Park**: Discover restored wetland habitats and local migratory birds.",
                "**Deer Park**: Jog around the lake and spot herds of deer inside the Hauz Khas green zone.",
                "**Okhla Sanctuary**: Visit the wetland sanctuary for bird-watching along the Yamuna River.",
                "**Nehru Park**: Relax in the large green park in Chanakyapuri, hosting music concerts.",
                "**Asola Bhatti**: Trek through the forest reserve trails to see the hidden blue lakes."
            ],
            "hi": [
                "**लोधी गार्डन**: 15वीं शताब्दी के भव्य ऐतिहासिक मकबरों से घिरे हरे-भरे मैदानों में टहलें।",
                "**सुंदर नर्सरी**: मुगल काल के सुंदर विरासत पार्क और पौधों की नर्सरी का अन्वेषण करें।",
                "**पंच इंद्रिय उद्यान (Garden of Five Senses)**: फव्वारों और मूर्तियों वाले सुंदर विषयगत उद्यान में आराम करें।",
                "**यमुना जैव विविधता पार्क**: पुनर्स्थापित आर्द्रभूमि आवासों और स्थानीय प्रवासी पक्षियों की खोज करें।",
                "**डियर पार्क**: हौज खास हरित क्षेत्र के भीतर झील के किनारे टहलें और हिरणों के झुंड देखें।",
                "**ओखला अभयारण्य**: यमुना नदी के किनारे पक्षियों को देखने के लिए आर्द्रभूमि अभयारण्य का दौरा करें।",
                "**नेहरू पार्क**: चाणक्यपुरी के बड़े हरे-भरे पार्क में आराम करें, जहां संगीत कार्यक्रम आयोजित होते हैं।",
                "**असोला भट्टी**: छिपी हुई नीली झीलों को देखने के लिए वन आरक्षित मार्गों पर ट्रेकिंग करें।"
            ],
            "te": [
                "**లోధి గార్డెన్స్**: 15వ శతాబ్దపు రాజుల సమాధులు కలిగిన పచ్చని పార్కులో ఉదయపు నడకను ఆస్వాదించండి.",
                "**సుందర్ నర్సరీ**: మొఘల్ కాలం నాటి చారిత్రక కట్టడాలు మరియు నర్సరీ గల పచ్చని పార్కును సందర్శించండి.",
                "**గార్డెన్ ఆఫ్ ఫైవ్ సెన్సెస్**: శిల్పాలు మరియు ఫౌంటైన్లతో అలంకరించబడిన అందమైన ఉద్యానవనంలో విశ్రాంతి తీసుకోండి.",
                "**యమునా బయోడైవర్సిటీ పార్క్**: పునరుద్ధరించబడిన తడి నేలలు మరియు వలస పక్షులను ఇక్కడ చూడండి.",
                "**డీర్ పార్క్**: హౌజ్ ఖాస్ సమీపంలోని పచ్చని పార్కులో జింకలను చూస్తూ సరస్సు చుట్టూ నడవండి.",
                "**ఓఖ్లా పక్షుల కేంద్రం**: యమునా నది ఒడ్డున ఉండే పక్షుల సంరక్షణ కేంద్రాన్ని సందర్శించండి.",
                "**నెహ్రూ పార్క్**: చాణక్యపురిలోని సంగీత కచేరీలు జరిగే విశాలమైన పచ్చని పార్కులో విశ్రాంతి తీసుకోండి.",
                "**అసోలా భట్టి**: అడవి మార్గాల గుండా ట్రెకింగ్ చేసి అందులోని అందమైన నీలి సరస్సులను వీక్షించండి."
            ]
        },
        "shopping": {
            "en": [
                "**Dilli Haat**: Shop for authentic regional handicrafts and taste foods from different states.",
                "**Sarojini Nagar**: Bargain for export-surplus clothing and trendy fashion accessories.",
                "**Khan Market**: Browse premium boutique stores, bookstores, and upscale cafes.",
                "**Chandni Chowk**: Explore the historic wholesale market for wedding attire, jewelry, and spices.",
                "**Janpath Market**: Shop for silver jewelry, handicrafts, and handloom fabrics near Connaught Place.",
                "**Lajpat Nagar Market**: Shop for traditional ethnic wear, fabrics, and footwear.",
                "**Karol Bagh**: Explore the busy shopping streets famous for jewelry and clothing showrooms.",
                "**Connaught Place**: Browse premium brand outlets and local handicraft shops in the circular market."
            ],
            "hi": [
                "**दिल्ली हाट**: प्रामाणिक क्षेत्रीय हस्तशिल्प की खरीदारी करें और विभिन्न राज्यों के व्यंजनों का स्वाद लें।",
                "**सरोजिनी नगर**: सस्ते ट्रेंडी कपड़ों और फैशन एक्सेसरीज के लिए मोलभाव करें।",
                "**खान मार्केट**: प्रीमियम बुटीक स्टोर्स, किताबों की दुकानों और महंगे कैफे का भ्रमण करें।",
                "**चांदनी चौक**: शादी के परिधानों, आभूषणों और मसालों के लिए ऐतिहासिक थोक बाजार का अन्वेषण करें।",
                "**जनपथ बाजार**: कनॉट प्लेस के पास चांदी के गहनों, हस्तशिल्प और हथकरघा कपड़ों की खरीदारी करें।",
                "**लाजपत नगर बाजार**: पारंपरिक जातीय परिधानों, कपड़ों और जूतों की खरीदारी करें।",
                "**करोल बाग**: गहनों और कपड़ों के शोरूम के लिए प्रसिद्ध व्यस्त शॉपिंग सड़कों का अन्वेषण करें।",
                "**कनॉट प्लेस**: गोलाकार बाजार में प्रीमियम ब्रांड आउटलेट्स और स्थानीय हस्तशिल्प दुकानों का भ्रमण करें।"
            ],
            "te": [
                "**ఢిల్లీ హాట్**: భారతదేశంలోని వివిధ రాష్ట్రాల చేతివృత్తుల వస్తువులు మరియు సాంప్రదాయ వంటకాలను ఇక్కడ కొనుగోలు చేయండి.",
                "**సరోజినీ నగర్**: అతి తక్కువ ధరలలో లభించే ఆధునిక దుస్తులు మరియు వస్తువులను ఇక్కడ బేరమాడి కొనుగోలు చేయండి.",
                "**ఖాన్ మార్కెట్**: అత్యంత విలాసవంతమైన దుకాణాలు, పుస్తకాల షాపులు మరియు కేఫ్‌లను ఇక్కడ సందర్శించండి.",
                "**చాందినీ చౌక్**: పెళ్లి బట్టలు, నగలు మరియు మసాలాలకు ప్రసిద్ధి చెందిన చారిత్రక రద్దీ మార్కెట్ ను అన్వేషించండి.",
                "**జన్‌పథ్ మార్కెట్**: కన్నాట్ ప్లేస్ సమీపంలోని వెండి నగలు, హస్తకళల వస్త్రాల షాపింగ్ కోసం ఇక్కడికి వెళ్ళండి.",
                "**లాజ్‌పత్ నగర్ మార్కెట్**: సాంప్రదాయ భారతీయ దుస్తులు, బట్టలు మరియు చెప్పుల కొనుగోలు కోసం ఈ మార్కెట్ ను సందర్శించండి.",
                "**కరోల్ బాగ్**: బంగారం మరియు వస్త్రాల షోరూమ్‌లకు ప్రసిద్ధి చెందిన రద్దీ వీధులను సందర్శించండి.",
                "**కన్నాట్ ప్లేస్**: వృత్తాకారంలో ఉండే ఈ చారిత్రక మార్కెట్ లో బ్రాండెడ్ వస్తువులు మరియు చేనేత దుకాణాలను సందర్శించండి."
            ]
        },
        "history": {
            "en": [
                "**Qutub Minar**: View the iconic 73-meter brick victory tower built in the 12th century.",
                "**Humayun's Tomb**: Visit the grand garden tomb that inspired the Taj Mahal architecture.",
                "**Purana Qila**: Explore the 16th-century stone fort and attend the evening sound and light show.",
                "**Red Fort**: Visit the majestic Mughal-era fort complex built of red sandstone.",
                "**India Gate**: Pay respects at the national war memorial arch dedicated to soldiers.",
                "**Safdarjung Tomb**: Admire the late Mughal-style marble and sandstone garden mausoleum.",
                "**Hauz Khas Fort**: Explore the ruins of the medieval college and lake built during the Delhi Sultanate.",
                "**Agrasen ki Baoli**: Visit the unique protected stepwell featuring 103 steps in the heart of Delhi."
            ],
            "hi": [
                "**कुतुब मीनार**: 12वीं शताब्दी में निर्मित 73 मीटर ऊंची ऐतिहासिक ईंटों की विजय मीनार को देखें।",
                "**हुमायूं का मकबरा**: ताज महल की वास्तुकला को प्रेरित करने वाले भव्य उद्यान मकबरे के दर्शन करें।",
                "**पुराना किला**: 16वीं शताब्दी के पत्थर के किले का अन्वेषण करें और शाम को लाइट एंड साउंड शो देखें।",
                "**लाल किला**: लाल बलुआ पत्थर से बने शानदार मुगल काल के किला परिसर का दौरा करें।",
                "**इंडिया गेट**: सैनिकों को समर्पित राष्ट्रीय युद्ध स्मारक मेहराब पर श्रद्धांजलि अर्पित करें।",
                "**सफदरजंग का मकबरा**: देर से बनी मुगल शैली के संगमरमर और बलुआ पत्थर के उद्यान मकबरे की प्रशंसा करें।",
                "**हौज खास किला**: दिल्ली सल्तनत के दौरान बने मध्यकालीन कॉलेज और झील के खंडहरों का अन्वेषण करें।",
                "**अग्रसेन की बावली**: दिल्ली के केंद्र में स्थित 103 सीढ़ियों वाली अनोखी संरक्षित बावली (स्टेपवेल) का दौरा करें।"
            ],
            "te": [
                "**కుతుబ్ మినార్**: 12వ శతాబ్దంలో ఇటుకలతో నిర్మించబడిన 73 మీటర్ల ఎత్తైన చారిత్రక విజయ స్తూపాన్ని వీక్షించండి.",
                "**హుమాయూన్ సమాధి**: తాజ్ మహల్ నిర్మాణ శైలికి స్ఫూర్తిగా నిలిచిన అద్భుతమైన మొఘల్ ఉద్యానవన సమాధిని సందర్శించండి.",
                "**పురానా ఖిలా**: 16వ శతాబ్దపు చారిత్రక కోటను సందర్శించి సాయంత్రం జరిగే లైట్ అండ్ సౌండ్ షోను తిలకించండి.",
                "**ఎర్రకోట**: ఎర్రటి ఇసుక రాయితో మొఘల్ కాలంలో నిర్మించబడిన అద్భుత కోటను సందర్శించండి.",
                "**ఇండియా గేట్**: దేశం కోసం ప్రాణాలర్పించిన అమరవీరుల జ్ఞాపకార్థం నిర్మించిన యుద్ధ స్మారకాన్ని సందర్శించండి.",
                "**సఫ్దర్‌జంగ్ సమాధి**: మొఘల్ శైలిలో నిర్మించబడిన అందమైన పాలరాతి మరియు ఇసుకరాతి సమాధిని సందర్శించండి.",
                "**హౌజ్ ఖాస్ కోట**: ఢిల్లీ సుల్తానుల కాలం నాటి చారిత్రక కళాశాల శిథిలాలను మరియు సరస్సును అన్వేషించండి.",
                "**అగ్రసేన్ కీ బావోలి**: ఢిల్లీ నడిబొడ్డున ఉన్న 103 మెట్లు గల చారిత్రక మెట్ల బావిని సందర్శించండి."
            ]
        },
        "default": {
            "en": [
                "**Red Fort**: Visit the primary monument of Mughal power in Old Delhi.",
                "**India Gate**: Walk along Rajpath and view the War Memorial.",
                "**Chandni Chowk**: Stroll in the historic market and try local street sweets.",
                "**Qutub Minar**: Explore the ancient ruins and the rust-free Iron Pillar.",
                "**Humayun's Tomb**: Walk around the beautiful Persian-style charbagh gardens.",
                "**Dilli Haat**: Shop for regional crafts and enjoy state cuisines.",
                "**Lotus Temple**: Experience silence and meditate in the white marble hall.",
                "**Bangla Sahib**: Visit the holy pond and participate in the community kitchen service."
            ],
            "hi": [
                "**लाल किला**: पुरानी दिल्ली में मुगल सत्ता के प्रमुख ऐतिहासिक स्मारक के दर्शन करें।",
                "**इंडिया गेट**: राजपथ पर टहलें और राष्ट्रीय युद्ध स्मारक का दृश्य देखें।",
                "**चांदनी चौक**: ऐतिहासिक बाजार में घूमें और स्थानीय स्ट्रीट मिठाइयों का स्वाद लें।",
                "**कुतुब मीनार**: प्राचीन खंडहरों और जंग-मुक्त लोहे के खंभे का अन्वेषण करें।",
                "**हुमायूं का मकबरा**: सुंदर फारसी शैली के चारबाग उद्यानों में टहलें।",
                "**दिल्ली हाट**: क्षेत्रीय शिल्पों की खरीदारी करें और राज्यों के व्यंजनों का आनंद लें।",
                "**लोटस टेम्पल**: सफेद संगमरमर के हॉल में मौन का अनुभव करें और ध्यान लगाएं।",
                "**बंगला साहिब**: पवित्र सरोवर के दर्शन करें और लंगर सेवा में भाग लें।"
            ],
            "te": [
                "**ఎర్రకోట**: పాత ఢిల్లీలోని మొఘల్ సామ్రాజ్యానికి చిహ్నమైన ఎర్రకోటను సందర్శించండి.",
                "**ఇండియా గేట్**: రాజ్‌పథ్ వెంబడి నడుస్తూ యుద్ధ స్మారకాన్ని వీక్షించండి.",
                "**చాందినీ చౌక్**: చారిత్రక మార్కెట్లో విహరిస్తూ స్థానిక మిఠాయిలను ఆస్వాదించండి.",
                "**కుతుబ్ మినార్**: పురాతన కట్టడాలను మరియు ఇనుప స్తంభాన్ని అన్వేషించండి.",
                "**హుమాయూన్ సమాధి**: పర్షియన్ శైలిలో ఉండే అందమైన చార్‌బాగ్ తోటలలో విహరించండి.",
                "**ఢిల్లీ హాట్**: వివిధ రాష్ట్రాల హస్తకళల వస్తువులను మరియు వంటకాలను ఆస్వాదించండి.",
                "**లోటస్ టెంపుల్**: తెల్లటి పాలరాతి మందిరంలో ప్రశాంతమైన ధ్యాన అనుభూతిని పొందండి.",
                "**బంగ్లా సాహిబ్**: పవిత్ర కోనేరును దర్శించి ఉచిత లంగర్ సేవలో పాల్గొనండి."
            ]
        }
    },
    "chennai": {
        "temples": {
            "en": [
                "**Kapaleeshwarar**: Visit the 7th-century Dravidian temple dedicated to Lord Shiva in Mylapore.",
                "**Parthasarathy**: Explore the ancient temple in Triplicane dedicated to Lord Krishna.",
                "**Ashtalakshmi**: Visit the unique coastal temple dedicated to Goddess Lakshmi in Besant Nagar.",
                "**Vadapalani Murugan**: Visit the famous temple dedicated to Lord Murugan, hosting weddings daily.",
                "**Marundeeswarar**: Explore the temple dedicated to Shiva as the healer, known for curing illnesses.",
                "**Kalikambal**: Visit the historic temple in George Town, visited by Shivaji Maharaj in the 17th century.",
                "**St. Thomas Mount**: Climb the historical hill shrine built over the place of St. Thomas martyrdom.",
                "**Santhome Cathedral**: Visit the majestic neo-Gothic basilica built over the tomb of St. Thomas."
            ],
            "hi": [
                "**कपालेश्वर**: मयलापुर में भगवान शिव को समर्पित 7वीं शताब्दी के द्रविड़ शैली के मंदिर के दर्शन करें।",
                "**पार्थसारथी**: ट्रिप्लिकेन में भगवान कृष्ण को समर्पित प्राचीन मंदिर का अन्वेषण करें।",
                "**अष्टलक्ष्मी**: बेसेंट नगर में समुद्र तट पर स्थित देवी लक्ष्मी के अनोखे मंदिर के दर्शन करें।",
                "**वडपलानी मुरुगन**: भगवान मुरुगन को समर्पित प्रसिद्ध मंदिर के दर्शन करें, जहां दैनिक विवाह होते हैं।",
                "**मरुन्देश्वरर**: स्वास्थ्य के देवता के रूप में शिव को समर्पित मंदिर का अन्वेषण करें, जो बीमारियों को ठीक करने के लिए प्रसिद्ध है।",
                "**कालिकांबल**: जॉर्ज टाउन में स्थित ऐतिहासिक मंदिर के दर्शन करें, जहां 17वीं शताब्दी में शिवाजी महाराज आए थे।",
                "**सेंट थॉमस माउंट**: सेंट थॉमस की शहादत के स्थान पर बने ऐतिहासिक पहाड़ी मंदिर पर चढ़ें।",
                "**संथोम कैथेड्रल**: सेंट थॉमस की कब्र पर बने भव्य नियो-गोथिक शैली के बेसिलिका के दर्शन करें।"
            ],
            "te": [
                "**కపాలీశ్వర ఆలయం**: మైలాపూర్‌లో ద్రావిడ శైలిలో నిర్మించబడిన 7వ శతాబ్దపు ప్రసిద్ధ శివాలయాన్ని సందర్శించండి.",
                "**పార్థసారథి ఆలయం**: ట్రిప్లికేన్‌లో విష్ణుమూర్తికి అంకితం చేయబడిన పురాతన ఆలయాన్ని అన్వేషించండి.",
                "**అష్టలక్ష్మి దేవాలయం**: బెసెంట్ నగర్ సముద్ర తీరంలో వెలసిన లక్ష్మీ దేవి ఆలయాన్ని సందర్శించండి.",
                "**వడపళని మురుగన్ ఆలయం**: నిత్య కళ్యాణాలతో సందడిగా ఉండే మురుగన్ ప్రసిద్ధ ఆలయాన్ని సందర్శించండి.",
                "**మరుందీశ్వర ఆలయం**: వైద్యునిగా శివుడిని పూజించే పురాతన ఆలయాన్ని అన్వేషించండి.",
                "**కాళికాంబాల్ ఆలయం**: జార్జ్ టౌన్ లోని చారిత్రక ఆలయం, దీనిని 17వ శతాబ్దంలో శివాజీ మహారాజ్ సందర్శించారు.",
                "**సెయింట్ థామస్ మౌంట్**: సెయింట్ థామస్ అమరవీరుడైన కొండపై నిర్మించిన చారిత్రక చర్చిని సందర్శించండి.",
                "**శాంతోమ్ కేథడ్రల్**: సెయింట్ థామస్ సమాధిపై నిర్మించబడిన అద్భుత శాంతోమ్ చర్చిని సందర్శించండి."
            ]
        },
        "food": {
            "en": [
                "**Idli Dosa**: Eat soft steamed Idlis and ghee paper roast Dosa at Murugan Idli Shop.",
                "**Chettinad Cuisine**: Savor spicy traditional curries and pepper chicken at local messes.",
                "**Filter Coffee**: Drink the iconic frothy filter coffee served in brass tumblers at Mylapore.",
                "**Marina Street Eats**: Relish spicy local Sundal (chickpea snack) and fresh fried fish on the beach.",
                "**Buhari Biryani**: Try the famous spicy mutton biryani at Buhari, the birthplace of Chicken 65.",
                "**Burmese Atho**: Savor unique street-style garlic-noodles in the streets of North Chennai.",
                "**Traditional Mess**: Experience a complete lunch feast served on a banana leaf at a local mess.",
                "**Jigarthanda**: Enjoy the cool sweet drink made of milk, almond gum, and sarsaparilla syrup."
            ],
            "hi": [
                "**इडली डोसा**: मुरुगन इडली शॉप में नरम इडली और घी से बनी पेपर रोस्ट डोसा का आनंद लें।",
                "**चेट्टीनाड व्यंजन**: स्थानीय भोजनालयों में तीखी पारंपरिक करी और काली मिर्च चिकन का स्वाद लें।",
                "**फिल्टर कॉफी**: मयलापुर में पीतल के गिलासों में परोसी जाने वाली झागदार प्रसिद्ध फिल्टर कॉफी पिएं।",
                "**मरीना स्ट्रीट फूड**: समुद्र तट पर तीखे स्थानीय सुंदल (चने का नाश्ता) और ताजी तली हुई मछली का आनंद लें।",
                "**बुहारी बिरयानी**: चिकन 65 के जन्मस्थान बुहारी में प्रसिद्ध मसालेदार मटन बिरयानी का स्वाद लें।",
                "**बर्मी आथो**: उत्तर चेन्नई की सड़कों पर अनोखे स्ट्रीट-स्टाइल लहसुन-नूडल्स का स्वाद लें।",
                "**पारंपरिक मेस**: एक स्थानीय मेस में केले के पत्ते पर परोसे जाने वाले दोपहर के शाही भोजन का अनुभव करें।",
                "**जिगरथंडा**: दूध, बादाम गोंद और सिरप से बने ठंडे मीठे पेय का आनंद लें।"
            ],
            "te": [
                "**ఇడ్లీ దోస**: మరుగన్ ఇడ్లీ షాప్ లో దూది లాంటి ఇడ్లీలు మరియు నెయ్యి పేపర్ రోస్ట్ దోసలను ఆస్వాదించండి.",
                "**చెట్టినాడు వంటకాలు**: కారంగా ఉండే సాంప్రదాయ చెట్టినాడు వంటకాలను స్థానిక హోటళ్ళలో రుచి చూడండి.",
                "**ఫిల్టర్ కాఫీ**: మైలాపూర్‌లో ఇత్తడి గ్లాసులలో లభించే నురగలతో కూడిన సాంప్రదాయ కాఫీని తాగండి.",
                "**మరీనా బీచ్ స్నాక్స్**: సాయంత్రం బీచ్ వెంబడి లభించే వేడి వేడి సుండల్ మరియు చేపల వేపుడును ఆస్వాదించండి.",
                "**బుహారీ బిర్యానీ**: చికెన్ 65 కి జన్మస్థలమైన బుహారీ రెస్టారెంట్‌లో రుచికరమైన బిర్యానీని ప్రయత్నించండి.",
                "**బర్మీస్ అథో**: ఉత్తర చెన్నై వీధుల్లో లభించే ప్రత్యేకమైన బర్మీస్ నూడిల్స్ ని రుచి చూడండి.",
                "**సాంప్రదాయ భోజనం**: అరటి ఆకులో వడ్డించే సాంప్రదాయ భోజన విందును స్థానిక హోటల్లో అనుభవించండి.",
                "**జిగర్తాండ**: పాలు, బాదం జిగురు మరియు ఐస్ క్రీం లతో కూడిన చల్లని జిగర్తాండను ఆస్వాదించండి."
            ]
        },
        "nature": {
            "en": [
                "**Marina Beach**: Walk along the second longest urban beach in the world, enjoying the breeze.",
                "**Theosophical Society**: Relax under the shade of ancient trees in the peaceful botanical gardens.",
                "**Guindy National Park**: Visit the city forest reserve, home to deer and butterfly parks.",
                "**Elliot's Beach**: Spend a quiet evening at the clean sandy beach in Besant Nagar.",
                "**Pallikaranai Wetland**: Visit the natural marshland to watch migratory birds and aquatic flora.",
                "**Adyar Eco Park**: Explore the restored eco-park featuring rich coastal vegetation and bird trails.",
                "**Pulicat Lake**: Take a day trip to see the brackish water lagoon, famous for winter flamingos.",
                "**Semmozhi Poonga**: Walk through the well-manicured horticultural garden featuring exotic plants."
            ],
            "hi": [
                "**मरीना बीच**: दुनिया के दूसरे सबसे लंबे शहरी समुद्र तट पर हवा का आनंद लेते हुए टहलें।",
                "**थियोसोफिकल सोसाइटी**: शांत वानस्पतिक उद्यानों में प्राचीन पेड़ों की छाया में आराम करें।",
                "**गिंडी राष्ट्रीय उद्यान**: शहरी वन रिजर्व का दौरा करें, जो हिरणों और तितली पार्कों का घर है।",
                "**इलियट बीच**: बेसेंट नगर के साफ रेतीले समुद्र तट पर एक शांत शाम बिताएं।",
                "**पल्लिकरनई आर्द्रभूमि**: प्रवासी पक्षियों और जलीय वनस्पतियों को देखने के लिए प्राकृतिक दलदली भूमि पर जाएँ।",
                "**अड्यार इको पार्क**: तटीय वनस्पतियों और पक्षी मार्गों वाले पुनर्स्थापित इको-पार्क का अन्वेषण करें।",
                "**पुलिकट झील**: सर्दियों के राजहंसों (फ्लेमिंगो) के लिए प्रसिद्ध खारे पानी की झील देखने के लिए एक दिवसीय यात्रा करें।",
                "**सेम्मोझी पूंगा**: विदेशी पौधों वाले अच्छी तरह से बनाए गए बागवानी उद्यान में टहलें।"
            ],
            "te": [
                "**మరీనా బీచ్**: ప్రపంచంలోనే రెండవ అతిపెద్ద సముద్ర తీరమైన మరీనా బీచ్ వెంబడి నడకను ఆస్వాదించండి.",
                "**థియోసాఫికల్ సొసైటీ**: ప్రశాంతమైన వాతావరణంలో పురాతన వృక్షాల నీడన గల తోటలలో విశ్రాంతి తీసుకోండి.",
                "**గిండీ నేషనల్ పార్క్**: నగరంలోనే ఉన్న అడవిని సందర్శించి జింకలను మరియు పక్షులను వీక్షించండి.",
                "**ఇలియట్స్ బీచ్**: బెసెంట్ నగర్ లో ఉండే ప్రశాంతమైన సముద్ర తీరంలో సాయంత్రం వేళ గడపండి.",
                "**పల్లికరణై తడినేలలు**: వలస పక్షులు వచ్చే సహజ సిద్ధమైన పల్లికరణై సరస్సును సందర్శించండి.",
                "**అడయార్ ఎకో పార్క్**: అందమైన చెట్లు మరియు పక్షుల మార్గాలు గల ఈ పార్కును సందర్శించండి.",
                "**పులికాట్ సరస్సు**: చలికాలంలో వలస వచ్చే ఫ్లెమింగో పక్షులకు ప్రసిద్ధి చెందిన పులికాట్ సరస్సుకు విహారయాత్ర చేయండి.",
                "**సెమ్మొళి పూంగా**: నగర నడిబొడ్డున ఉన్న అందమైన బొటానికల్ గార్డెన్ లో విహరించండి."
            ]
        },
        "shopping": {
            "en": [
                "**T Nagar**: Shop at T Nagar, the largest market hub for Kanchipuram silk sarees and gold jewelry.",
                "**Pondy Bazaar**: Browse street shops for clothing, footwear, toys, and local artifacts.",
                "**Spencer Plaza**: Visit one of India's oldest shopping malls for leather goods and curios.",
                "**Sowcarpet**: Explore the bustling streets famous for North Indian attire and wholesale goods.",
                "**Ritchie Street**: Browse the busy electronic market lane for accessories and gadgets.",
                "**Cotton Street**: Browse the collection of export fabrics, cotton goods, and handloom materials.",
                "**Mylapore Bazaar**: Shop for traditional metal lamps, flower garlands, and prayer items near the temple.",
                "**Express Avenue**: Shop for international fashion brands and visit the large food court."
            ],
            "hi": [
                "**टी नगर**: कांचीपुरम रेशमी साड़ियों और सोने के आभूषणों के सबसे बड़े बाजार टी नगर में खरीदारी करें।",
                "**पोंडी बाजार**: कपड़ों, जूतों, खिलौनों और स्थानीय कलाकृतियों के लिए स्ट्रीट दुकानों का भ्रमण करें।",
                "**स्पेंसर प्लाजा**: चमड़े के सामान और प्राचीन वस्तुओं के लिए भारत के सबसे पुराने शॉपिंग मॉल में से एक का दौरा करें।",
                "**सॉकरपेट**: उत्तर भारतीय परिधानों और थोक सामानों के लिए प्रसिद्ध व्यस्त सड़कों का अन्वेषण करें।",
                "**रिची स्ट्रीट**: सामान और गैजेट्स के लिए व्यस्त इलेक्ट्रॉनिक बाजार का भ्रमण करें।",
                "**कॉटन स्ट्रीट**: निर्यात किए गए कपड़ों, सूती सामानों और हथकरघा सामग्रियों के संग्रह को देखें।",
                "**मयलापुर बाजार**: मंदिर के पास पारंपरिक धातु के दीयों, फूलों के हार और पूजा सामग्री की खरीदारी करें।",
                "**एक्सप्रेस एवेन्यू**: अंतर्राष्ट्रीय फैशन ब्रांडों की खरीदारी करें और बड़े फूड कोर्ट का दौरा करें।"
            ],
            "te": [
                "**టీ నగర్**: కంచి పట్టు చీరలు మరియు బంగారు ఆభరణాలకు ప్రసిద్ధి చెందిన టీ నగర్ లో షాపింగ్ చేయండి.",
                "**పాండీ బజార్**: బట్టలు, చెప్పులు మరియు హస్తకళల వస్తువుల వీధి దుకాణాలను అన్వేషించండి.",
                "**స్పెన్సర్ ప్లాజా**: భారతదేశంలోనే అత్యంత పురాతనమైన షాపింగ్ మాల్ ను సందర్శించి చర్మ ఉత్పత్తులను కొనుగోలు చేయండి.",
                "**సౌకార్‌పేట్**: వివిధ రకాల హోల్‌సేల్ బట్టలు మరియు వస్తువులు దొరికే రద్దీ వీధులను సందర్శించండి.",
                "**రిచీ స్ట్రీట్**: ఎలక్ట్రానిక్ వస్తువుల కొనుగోలు కోసం ఈ మార్కెట్ వీధిని సందర్శించండి.",
                "**కాటన్ స్ట్రీట్**: ఎగుమతి నాణ్యత కలిగిన కాటన్ దుస్తులు మరియు చేనేత వస్త్రాలను ఇక్కడ కొనుగోలు చేయండి.",
                "**మైలాపూర్ బజార్**: దేవాలయం సమీపంలో లభించే ఇత్తడి పూజా సామాగ్రి మరియు పూల మాలలను కొనుగోలు చేయండి.",
                "**ఎక్స్‌ప్రెస్ అవెన్యూ**: విభిన్న రకాల బ్రాండెడ్ వస్తువులు మరియు ఫుడ్ కోర్ట్ గల మాల్ ని సందర్శించండి."
            ]
        },
        "history": {
            "en": [
                "**Fort St. George**: Explore the first English fortress in India, built in 1644, and its museum.",
                "**Government Museum**: Visit the museum complex in Egmore, housing the world's best bronze gallery.",
                "**DakshinaChitra**: Explore the living history museum showcasing traditional homes of South Indian states.",
                "**Mahabalipuram**: Take a day trip to explore the UNESCO rock-cut shore temples and monuments.",
                "**Ripon Building**: Admire the Indo-Saracenic neoclassical style architecture of the corporation seat.",
                "**Senate House**: View the historic Senate House inside the Madras University campus.",
                "**Valluvar Kottam**: Visit the chariot-shaped monument dedicated to the Tamil poet Thiruvalluvar.",
                "**Vivekananda House**: Visit the castle where Swami Vivekananda stayed, now housing a museum."
            ],
            "hi": [
                "**फोर्ट सेंट जॉर्ज**: 1644 में निर्मित भारत के पहले ब्रिटिश किले और उसके संग्रहालय का अन्वेषण करें।",
                "**सरकारी संग्रहालय**: एगमोर में स्थित संग्रहालय का दौरा करें, जिसमें दुनिया की सबसे अच्छी कांस्य गैलरी है।",
                "**दक्षिणाचित्र**: दक्षिण भारतीय राज्यों के पारंपरिक घरों को प्रदर्शित करने वाले इतिहास संग्रहालय का अन्वेषण करें।",
                "**महाबलीपुरम**: यूनेस्को की चट्टानों को काटकर बनाए गए तटीय मंदिरों और स्मारकों का अन्वेषण करने के लिए एक दिवसीय यात्रा करें।",
                "**रिपन बिल्डिंग**: चेन्नई नगर निगम के इंडो-सारसेनिक नवशास्त्रीय शैली की वास्तुकला की प्रशंसा करें।",
                "**सीनेट हाउस**: मद्रास विश्वविद्यालय परिसर के भीतर ऐतिहासिक सीनेट हाउस को देखें।",
                "**वल्लुवर कोट्टम**: तमिल कवि तिरुवल्लुवर को समर्पित रथ के आकार के स्मारक का दौरा करें।",
                "**विवेकानंद हाउस**: उस महल का दौरा करें जहां स्वामी विवेकानंद ठहरे थे, जो अब एक संग्रहालय है।"
            ],
            "te": [
                "**ఫోర్ట్ సెయింట్ జార్జ్**: 1644లో నిర్మించబడిన భారతదేశపు మొదటి బ్రిటిష్ కోటను మరియు దాని మ్యూజియాన్ని అన్వేషించండి.",
                "**గవర్నమెంట్ మ్యూజియం**: ఎగ్మోర్ లోని పురాతన మ్యూజియాన్ని సందర్శించి అందులోని అందమైన కంచు శిల్పాలను వీక్షించండి.",
                "**దక్షిణచిత్ర**: దక్షిణ భారతదేశ సంస్కృతిని ప్రతిబింబించే చారిత్రక ఇళ్ళ నమూనాలు గల మ్యూజియాన్ని సందర్శించండి.",
                "**మహాబలిపురం**: యునెస్కో గుర్తింపు పొందిన సముద్ర తీర రథ ఆలయాలను సందర్శించడానికి ఒక రోజు విహారయాత్ర చేయండి.",
                "**రిపన్ బిల్డింగ్**: కార్పొరేషన్ కార్యాలయం యొక్క నియోక్లాసికల్ నిర్మాణ శైలి భవనాన్ని తిలకించండి.",
                "**సెనేట్ హౌస్**: మద్రాస్ యూనివర్సిటీ ఆవరణలోని చారిత్రక సెనేట్ హౌస్ భవనాన్ని వీక్షించండి.",
                "**వళ్ళువర్ కొట్టం**: తమిళ కవి తిరువళ్ళువర్ జ్ఞాపకార్థం రథం ఆకృతిలో నిర్మించిన కట్టడాన్ని సందర్శించండి.",
                "**వివేకానంద హౌస్**: స్వామి వివేకానంద చెన్నై పర్యటనలో నివసించిన చారిత్రక గృహాన్ని సందర్శించండి."
            ]
        },
        "default": {
            "en": [
                "**Marina Beach**: Walk along the shore and watch the lighthouse lit up at night.",
                "**Kapaleeshwarar**: Visit the landmark temple and try South Indian coffee nearby.",
                "**Filter Coffee**: Savor local breakfast idlis and fresh filter coffee.",
                "**Fort St. George**: Explore the historical ramparts and view old weapons in the museum.",
                "**Mahabalipuram**: Drive along the scenic East Coast Road to see the Shore Temple.",
                "**DakshinaChitra**: Tour the heritage homes and participate in craft workshops.",
                "**T Nagar**: Browse the busy shopping lanes for silk fabrics and gold showrooms.",
                "**Elliot's Beach**: Enjoy the evening breeze and try fried fish at street side stalls."
            ],
            "hi": [
                "**मरीना बीच**: समुद्र तट पर टहलें और रात में जलने वाले लाइटहाउस (प्रकाशस्तंभ) को देखें।",
                "**कपालेश्वर**: ऐतिहासिक मंदिर के दर्शन करें और पास में दक्षिण भारतीय कॉफी का स्वाद लें।",
                "**फिल्टर कॉफी**: स्थानीय नाश्ते इडली और ताजी फिल्टर कॉफी का आनंद लें।",
                "**फोर्ट सेंट जॉर्ज**: ऐतिहासिक प्राचीर का अन्वेषण करें और संग्रहालय में पुराने हथियारों को देखें।",
                "**महाबलीपुरम**: शोर टेम्पल (तटीय मंदिर) देखने के लिए सुंदर ईस्ट कोस्ट रोड पर ड्राइव करें।",
                "**दक्षिणाचित्र**: विरासत घरों का दौरा करें और शिल्प कार्यशालाओं में भाग लें।",
                "**टी नगर**: रेशमी कपड़ों और सोने के शोरूम के लिए व्यस्त शॉपिंग गलियों में घूमें।",
                "**इलियट बीच**: शाम की हवा का आनंद लें और सड़क किनारे के स्टालों पर तली हुई मछली का स्वाद लें।"
            ],
            "te": [
                "**మరీనా బీచ్**: సముద్ర తీరం వెంబడి నడుస్తూ సాయంత్రం వేళ లైట్‌హౌస్ కాంతులను వీక్షించండి.",
                "**కపాలీశ్వర ఆలయం**: ఈ మైలాపూర్ దేవాలయాన్ని దర్శించి సమీపంలో ఫిల్టర్ కాఫీ తాగండి.",
                "**ఫిల్టర్ కాఫీ**: ఉదయాన్నే వేడివేడి ఇడ్లీలు తిని ఫిల్టర్ కాఫీతో రోజును ప్రారంభించండి.",
                "**ఫోర్ట్ సెయింట్ జార్జ్**: చారిత్రక కోటను అన్వేషించి మ్యూజియంలోని పురాతన ఆయుధాలను వీక్షించండి.",
                "**మహాబలిపురం**: ఈస్ట్ కోస్ట్ రోడ్డు గుండా ప్రయాణించి సముద్ర తీర ఆలయాలను సందర్శించండి.",
                "**దక్షిణచిత్ర**: సాంప్రదాయ ఇళ్ళను సందర్శించి హస్తకళల తయారీలో పాల్గొనండి.",
                "**టీ నగర్**: పట్టు చీరలు మరియు బంగారు ఆభరణాల కోసం ఇక్కడి బజార్లలో షాపింగ్ చేయండి.",
                "**ఇలియట్స్ బీచ్**: సాయంత్రం చల్లని గాలిని ఆస్వాదిస్తూ బీచ్ వద్ద లభించే చేపల ఫ్రైని రుచి చూడండి."
            ]
        }
    },
    "ahmedabad": {
        "temples": {
            "en": [
                "**Akshardham**: Visit the massive sandstone temple complex showcasing cultural exhibitions.",
                "**Hutheesing Jain**: Visit the beautiful temple built in 1848, famous for its stone carvings.",
                "**Jama Masjid**: Explore the historic 15th-century mosque built using yellow sandstone.",
                "**Bhadrakali**: Pay respects at the temple of the city's patron goddess, located inside Bhadra Fort.",
                "**ISKCON Ahmedabad**: Explore the temple complex featuring beautifully painted ceilings and gardens.",
                "**Camp Hanuman**: Visit the highly popular temple dedicated to Hanuman inside the cantonment area.",
                "**Trimandir**: Visit the large non-sectarian temple in Adalaj promoting spiritual harmony.",
                "**Sidi Saiyyed Mosque**: Admire the world-famous stone lattice window carvings (Jali) in the mosque."
            ],
            "hi": [
                "**अक्षरधाम**: सांस्कृतिक प्रदर्शनियों को प्रदर्शित करने वाले विशाल बलुआ पत्थर के मंदिर परिसर के दर्शन करें।",
                "**हठीसिंह जैन**: 1848 में निर्मित सुंदर मंदिर के दर्शन करें, जो अपनी पत्थर की नक्काशी के लिए प्रसिद्ध है।",
                "**जामा मस्जिद**: पीले बलुआ पत्थर से बनी ऐतिहासिक 15वीं शताब्दी की मस्जिद का अन्वेषण करें।",
                "**भद्रकाली**: भद्र किले के भीतर स्थित शहर की संरक्षक देवी के मंदिर में माथा टेकें।",
                "**इस्कॉन अहमदाबाद**: सुंदर चित्रित छतों और बगीचों वाले मंदिर परिसर का भ्रमण करें।",
                "**कैंप हनुमान**: छावनी क्षेत्र के भीतर हनुमान जी को समर्पित अत्यधिक लोकप्रिय मंदिर के दर्शन करें।",
                "**त्रिमंदिर**: आध्यात्मिक सद्भाव को बढ़ावा देने वाले अदालज में स्थित विशाल मंदिर के दर्शन करें।",
                "**सिदी सैयद मस्जिद**: मस्जिद में विश्व प्रसिद्ध पत्थर की जालीदार नक्काशी (जाली) की प्रशंसा करें।"
            ],
            "te": [
                "**అక్షరధామ్ ఆలయం**: గాంధీనగర్ లోని ఎర్రటి రాయితో నిర్మించబడిన అద్భుత ఆధ్యాత్మిక ఆలయాన్ని సందర్శించండి.",
                "**హతీసింగ్ జైన్ ఆలయం**: 1848లో నిర్మించబడిన అద్భుత జైన్ ఆలయాన్ని సందర్శించి శిల్పకళను తిలకించండి.",
                "**జామా మసీదు**: పసుపు రంగు ఇసుక రాయితో కట్టిన చారిత్రక 15వ శతాబ్దపు మసీదును సందర్శించండి.",
                "**భద్రకాళి ఆలయం**: భద్ర కోట లోపల ఉండే గ్రామదేవత భద్రకాళి ఆలయాన్ని సందర్శించండి.",
                "**ఇస్కాన్ ఆలయం**: రంగురంగుల పెయింటింగ్స్ మరియు పూల తోటలతో అలరారే ఇస్కాన్ ఆలయాన్ని అన్వేషించండి.",
                "**క్యాంప్ హనుమాన్ ఆలయం**: సైనిక కంటోన్మెంట్ ఏరియాలో ఉన్న అత్యంత ప్రసిద్ధ హనుమాన్ ఆలయాన్ని సందర్శించండి.",
                "**త్రిమందిరం**: అదాలజ్ సమీపంలో నిర్మించిన అన్ని మతాల సమ్మేళన ప్రార్థనా మందిరాన్ని సందర్శించండి.",
                "**సిదీ సయ్యద్ మసీదు**: పచ్చరాతి తో కట్టిన కిటికీలపై చేసిన ప్రపంచ ప్రసిద్ధ శిల్పకళా జాలీలను వీక్షించండి."
            ]
        },
        "food": {
            "en": [
                "**Gujarati Thali**: Eat a sweet and savory vegetarian Gujarati Thali at Agashiye or Vishalla.",
                "**Khaman Dhokla**: Sample soft steamed Khaman and Dhokla served with spicy green chutneys.",
                "**Manek Chowk**: Eat fusion street foods like Gwalior Dosa and Chocolate Sandwich at the night market.",
                "**Fafda Jalebi**: Try crispy savory Fafda and sweet hot Jalebi at the historic Chandravilas shop.",
                "**Induben Khakhra**: Taste various flavored Khakhra and local snacks at the famous store.",
                "**Dal Wada**: Savor hot spicy yellow-lentil fritters served with green chilies at crossroads.",
                "**Lucky Tea Stall**: Experience maskabun and tea inside the cafe built around historic graves.",
                "**Ashrafi Kulfi**: Relish traditional creamy kulfi inside clay cups at the famous local shop."
            ],
            "hi": [
                "**गुजराती थाली**: अगाशिये या विशाला में मीठी और नमकीन शाकाहारी गुजराती थाली का आनंद लें।",
                "**खमन ढोकला**: तीखी हरी चटनी के साथ परोसे जाने वाले नरम खमन और ढोकला का स्वाद लें।",
                "**मानेक चौक**: रात के बाजार में ग्वालियर डोसा और चॉकलेट सैंडविच जैसे फ्यूजन स्ट्रीट फूड खाएं।",
                "**फाफड़ा जलेबी**: ऐतिहासिक चंद्रविलास दुकान पर कुरकुरे फाफड़ा और गरमा-गरम जलेबी का स्वाद लें।",
                "**इन्दुबेन खाखरा**: प्रसिद्ध दुकान पर विभिन्न स्वादों के खाखरा और स्थानीय स्नैक्स का स्वाद लें।",
                "**दाल वड़ा**: हरी मिर्च के साथ परोसे जाने वाले गरमा-गरम तीखे दाल के वड़ों का स्वाद लें।",
                "**लकी टी स्टॉल**: ऐतिहासिक कब्रों के चारों ओर बने कैफे में मस्काबन और चाय का अनुभव करें।",
                "**अशर्फी कुल्फी**: प्रसिद्ध स्थानीय दुकान पर मिट्टी के कपों में परोसी जाने वाली मलाईदार कुल्फी का आनंद लें।"
            ],
            "te": [
                "**గుజరాతీ థాలీ**: అగాశియే లేదా విశాల్లా హోటళ్ళలో సాంప్రదాయ గుజరాతీ శాకాహార భోజనాన్ని ఆస్వాదించండి.",
                "**ఖమన్ ధోక్లా**: ఆవిరితో ఉడికించిన మెత్తని ఖమన్ మరియు ధోక్లా పిండివంటలను రుచి చూడండి.",
                "**మానెక్ చౌక్**: రాత్రి పూట తినుబండారాల మార్కెట్ గా మారే ఇక్కడ చాక్లెట్ శాండ్‌విచ్ మరియు దోసలను ప్రయత్నించండి.",
                "**ఫాఫ్డా జిలేబీ**: చారిత్రక చంద్రవిలాస్ దుకాణంలో కరకరలాడే ఫాఫ్డా మరియు వేడివేడి జిలేబీలను రుచి చూడండి.",
                "**ఇందుబెన్ ఖాఖ్రా**: ప్రసిద్ధ షాపులో లభించే రకరకాల రుచుల ఖాఖ్రాలను మరియు స్నాక్స్ ని సేకరించండి.",
                "**దాల్ వడ**: రోడ్డు పక్కన పచ్చిమిరపకాయలతో వడ్డించే వేడి వేడి దాల్ వడలను ఆస్వాదించండి.",
                "**లక్కీ టీ స్టాల్**: చారిత్రక సమాధుల మధ్య నిర్మించిన ఈ ప్రసిద్ధ కేఫ్‌లో బన్ మస్కా మరియు చాయ్ తాగండి.",
                "**అష్రఫీ కుల్ఫీ**: మట్టి కప్పులలో లభించే చిక్కటి క్రీమ్ కుల్ఫీని ఈ ప్రసిద్ధ దుకాణంలో ఆస్వాదించండి."
            ]
        },
        "nature": {
            "en": [
                "**Kankaria Lake**: Take an evening walk around the lake, visit the zoo, and enjoy the balloon ride.",
                "**Sabarmati Riverfront**: Walk along the scenic concrete promenade by the river.",
                "**Parimal Garden**: Relax in the peaceful park featuring lotus ponds and brick walking tracks.",
                "**Thol Lake**: Take a day trip to the calm lake sanctuary, a paradise for bird-watchers.",
                "**Nalsarovar**: Visit the massive natural lake sanctuary, home to winter migratory birds.",
                "**Indroda Park**: Explore the dinosaur fossil park, often called India's Jurassic Park, in Gandhinagar.",
                "**Vastrapur Lake**: Walk around the beautiful lake featuring green lawns and open-air theater.",
                "**Law Garden Walk**: Take a peaceful evening walk through the green spaces near the handicraft market."
            ],
            "hi": [
                "**कांकरिया झील**: झील के चारों ओर शाम की सैर करें, चिड़ियाघर का दौरा करें और गुब्बारे की सवारी का आनंद लें।",
                "**साबरमती रिवरफ्रंट**: नदी के किनारे बने सुंदर कंक्रीट सैरगाह पर टहलें।",
                "**परिमल गार्डन**: कमल के तालाबों और चलने के रास्तों वाले इस शांत पार्क में आराम करें।",
                "**थोल झील**: पक्षी प्रेमियों के लिए स्वर्ग मानी जाने वाली इस शांत झील अभयारण्य की एक दिवसीय यात्रा करें।",
                "**नलसरोवर**: सर्दियों के प्रवासी पक्षियों के घर, इस विशाल प्राकृतिक झील अभयारण्य का दौरा करें।",
                "**इंद्रोदा पार्क**: गांधीनगर में स्थित डायनासोर जीवाश्म पार्क का अन्वेषण करें, जिसे भारत का जुरासिक पार्क भी कहा जाता है।",
                "**वस्त्रापुर झील**: हरे-भरे मैदानों और ओपन-एयर थिएटर वाली इस सुंदर झील के चारों ओर टहलें।",
                "**लॉ गार्डन वॉक**: हस्तशिल्प बाजार के पास स्थित हरित क्षेत्रों में एक शांतिपूर्ण शाम की सैर करें।"
            ],
            "te": [
                "**కంకరియా సరస్సు**: సరస్సు వెంబడి సాయంత్రం నడుస్తూ, అందులోని జూ మరియు బెలూన్ సవారీలను ఆస్వాదించండి.",
                "**సబర్మతి రివర్‌ఫ్రంట్**: నది పక్కనే నిర్మించిన అందమైన వాకింగ్ మార్గంలో నడకను ఆస్వాదించండి.",
                "**పరిమల్ గార్డెన్**: తామర కొలనులు మరియు నడక దారులతో కూడిన అందమైన పార్కులో విశ్రాంతి తీసుకోండి.",
                "**థోల్ సరస్సు**: పక్షుల వీక్షణకు ప్రసిద్ధి చెందిన ప్రశాంతమైన థోల్ సరస్సు సంరక్షణ కేంద్రాన్ని సందర్శించండి.",
                "**నల్‌సరోవర్**: చలికాలంలో వేలాది వలస పక్షులు వచ్చే గుజరాత్‌లోనే అతిపెద్ద పక్షుల సరస్సును సందర్శించండి.",
                "**ఇంద్రోదా పార్క్**: గాంధీనగర్ లో ఉండే డైనోసార్ శిలాజాల పార్కును (ఇండియా జురాసిక్ పార్క్) సందర్శించండి.",
                "**వస్త్రాపూర్ సరస్సు**: పచ్చని లాన్లు మరియు ఓపెన్ ఎయిర్ థియేటర్ గల ఈ అందమైన చెరువు చుట్టూ నడవండి.",
                "**లా గార్డెన్ వాక్**: బజార్ సమీపంలో ఉండే ఈ తోటలో ప్రశాంతమైన సాయంత్రపు నడకను ఆస్వాదించండి."
            ]
        },
        "shopping": {
            "en": [
                "**Law Garden**: Shop for traditional hand-embroidered mirrors work clothes and crafts at the night market.",
                "**Sindhi Market**: Explore the traditional market famous for block printed fabrics and dress materials.",
                "**Lal Darwaza**: Browse the busy street market for budget-friendly clothing and footwear.",
                "**Dhalgarwad**: Visit the historic market for traditional fabrics like Bandhani and Patola silks.",
                "**Raipur Darwaza**: Shop for local Gujarati sweets and savory snack items.",
                "**CG Road**: Shop at premium branded apparel outlets, jewelry showrooms, and malls.",
                "**Ahmedabad Haat**: Buy authentic handicrafts made by rural Gujarati artisans directly.",
                "**Ravivari Market**: Visit the historic Sunday flea market on the riverfront for old items and curios."
            ],
            "hi": [
                "**लॉ गार्डन**: रात के बाजार में पारंपरिक हाथ से कढ़ाई की हुई पोशाकें और हस्तशिल्प खरीदें।",
                "**सिंधी मार्केट**: ब्लॉक प्रिंटेड कपड़ों और परिधान सामग्रियों के लिए प्रसिद्ध पारंपरिक बाजार का दौरा करें।",
                "**लाल दरवाजा**: बजट के अनुकूल कपड़ों और जूतों के लिए व्यस्त स्ट्रीट मार्केट का भ्रमण करें।",
                "**ढालगरवाड़**: बांधनी और पटोला रेशम जैसे पारंपरिक कपड़ों के लिए ऐतिहासिक बाजार का दौरा करें।",
                "**रायपुर दरवाजा**: स्थानीय गुजराती मिठाइयों और नमकीन स्नैक्स की खरीदारी करें।",
                "**सीजे रोड**: प्रीमियम ब्रांडेड कपड़ों के आउटलेट, आभूषण शो रूम और मॉल में खरीदारी करें।",
                "**अहमदाबाद हाट**: ग्रामीण गुजराती कारीगरों द्वारा बनाए गए प्रामाणिक हस्तशिल्प सीधे खरीदें।",
                "**रविबारी बाजार**: पुरानी वस्तुओं और कलाकृतियों के लिए रिवरफ्रंट पर लगने वाले ऐतिहासिक रविवार पिस्सू बाजार का दौरा करें।"
            ],
            "te": [
                "**లా గార్డెన్**: ఇక్కడి నైట్ మార్కెట్లో సాంప్రదాయ గుజరాతీ అద్దాల డిజైన్ బట్టలు మరియు వస్తువులను కొనుగోలు చేయండి.",
                "**సింధి మార్కెట్**: వివిధ రకాల కాటన్ మరియు బ్లాక్ ప్రింట్ దుస్తుల అమ్మకాలకు ప్రసిద్ధి చెందిన పురాతన మార్కెట్ ను సందర్శించండి.",
                "**లాల్ దర్వాజా**: బడ్జెట్ ధరలలో లభించే దుస్తులు మరియు చెప్పుల కోసం ఇక్కడి వీధి మార్కెట్ ను సందర్శించండి.",
                "**ధాల్గర్వాడ్**: బంధాని మరియు పటోలా పట్టు చీరలకు ప్రసిద్ధి చెందిన చారిత్రక మార్కెట్ ను సందర్శించండి.",
                "**రాయ్‌పూర్ దర్వాజా**: స్థానిక గుజరాతీ తినుబండారాలు మరియు స్వీట్ల కొనుగోలు కోసం ఇక్కడికి వెళ్ళండి.",
                "**CG రోడ్**: బ్రాండెడ్ వస్త్రాల షోరూమ్‌లు మరియు నగల దుకాణాల కోసం ఇక్కడికి వెళ్ళండి.",
                "**అహ్మదాబాద్ హాట్**: గ్రామీణ గుజరాతీ కళాకారుల చేత తయారు చేయబడిన వస్తువులను నేరుగా కొనుగోలు చేయండి.",
                "**రవివారి మార్కెట్**: రివర్‌ఫ్రంట్ వద్ద ఆదివారం పూట జరిగే పురాతన వస్తువుల మార్కెట్ ను సందర్శించండి."
            ]
        },
        "history": {
            "en": [
                "**Sabarmati Ashram**: Visit Mahatma Gandhi's peaceful home on the banks of Sabarmati River, now a museum.",
                "**Adalaj Stepwell**: Explore the 15th-century stepwell, a marvel of Solanki style architecture.",
                "**Bhadra Fort**: Visit the historic fort built in 1411 and climb the Teen Darwaza gateway.",
                "**Calico Museum**: Tour the premier textile museum displaying rare fabrics and historic garments.",
                "**Sarkhej Roza**: Explore the elegant Sufi tomb complex featuring Hindu and Islamic architectural details.",
                "**Jhulta Minar**: Visit the Shaking Minarets of Sidi Bashir mosque, displaying an unsolved architectural mystery.",
                "**Old City Walk**: Join a heritage walking tour through the narrow lanes (Pols) of the old city.",
                "**Dada Harir**: Visit the deep, intricately carved five-story stone stepwell built in 1485."
            ],
            "hi": [
                "**साबरमती आश्रम**: साबरमती नदी के तट पर महात्मा गांधी के शांतिपूर्ण घर का दौरा करें, जो अब एक संग्रहालय है।",
                "**अदालज की बावड़ी (Adalaj Stepwell)**: सोलंकी शैली की वास्तुकला के चमत्कार, 15वीं शताब्दी की बावड़ी का अन्वेषण करें।",
                "**भद्रा किला**: 1411 में निर्मित ऐतिहासिक किले का दौरा करें और तीन दरवाजा गेटवे पर चढ़ें।",
                "**कैलिको संग्रहालय**: दुर्लभ कपड़ों और ऐतिहासिक परिधानों को प्रदर्शित करने वाले प्रमुख कपड़ा संग्रहालय का दौरा करें।",
                "**सरखेज रोजा**: हिंदू और इस्लामी स्थापत्य कला वाले सुंदर सूफी मकबरे परिसर का अन्वेषण करें।",
                "**झूलती मीनार**: सीदी बशीर मस्जिद की झूलती मीनारों के दर्शन करें, जो एक अनसुलझा स्थापत्य रहस्य है।",
                "**ओल्ड सिटी वॉक**: पुराने शहर की संकरी गलियों (पोल) से गुजरने वाली एक विरासत पैदल यात्रा में शामिल हों।",
                "**दादा हरीर**: 1485 में निर्मित पांच मंजिला गहरे, जटिल नक्काशीदार पत्थर के स्टेपवेल का दौरा करें।"
            ],
            "te": [
                "**సబర్మతి ఆశ్రమం**: సబర్మతి నది ఒడ్డున మహాత్మా గాంధీ నివసించిన ప్రశాంతమైన ఆశ్రమాన్ని మరియు మ్యూజియాన్ని సందర్శించండి.",
                "**అదాలజ్ మెట్ల బావి**: సోలంకీ శైలిలో 15వ శతాబ్దంలో నిర్మించబడిన అద్భుత మెట్ల బావిని సందర్శించండి.",
                "**భద్ర కోట**: 1411లో నిర్మించబడిన చారిత్రక కోటను మరియు పక్కనే ఉన్న తీన్ దర్వాజా ద్వారాన్ని సందర్శించండి.",
                "**కాలికో టెక్స్‌టైల్ మ్యూజియం**: గుజరాత్ చేనేత వస్త్రాలు మరియు పురాతన దుస్తుల మ్యూజియాన్ని సందర్శించండి.",
                "**సర్ఖేజ్ రోజా**: హిందూ మరియు ఇస్లామిక్ నిర్మాణ శైలి కలిగిన చారిత్రక సూఫీ సమాధుల సముదాయాన్ని అన్వేషించండి.",
                "**ఝుల్తా మినార్**: ఒకదానిని ఊపితే మరొకటి కదిలే ఇక్కడి చారిత్రక ఊగే మినార్ల వింతను చూడండి.",
                "**ఓల్డ్ సిటీ వాక్**: పాత నగరంలోని పోల్స్ అని పిలవబడే సన్నని వీధుల గుండా హెరిటేజ్ వాక్ చేయండి.",
                "**దాదా హరిర్**: 1485లో రాతితో నిర్మించిన ఐదు అంతస్తుల చారిత్రక లోతైన మెట్ల బావిని సందర్శించండి."
            ]
        },
        "default": {
            "en": [
                "**Sabarmati Ashram**: Visit the primary spiritual sanctuary of Mahatma Gandhi.",
                "**Adalaj Stepwell**: Admire the grand carving and stone columns of the stepwell.",
                "**Manek Chowk**: Savor the local street dishes at the late-night food court.",
                "**Sabarmati Riverfront**: Take a relaxing evening walk along the river promenade.",
                "**Law Garden**: Browse the colorful Gujarati handicraft market stalls.",
                "**Sidi Saiyyed**: Photograph the historic stone-carved window lattice work.",
                "**Sarkhej Roza**: Explore the majestic tomb and ancient lake structures.",
                "**Calico Museum**: Visit the famous repository of Indian textile heritage."
            ],
            "hi": [
                "**साबरमती आश्रम**: महात्मा गांधी के प्राथमिक आध्यात्मिक अभयारण्य का दौरा करें।",
                "**अदालज की बावड़ी**: बावड़ी की भव्य नक्काशी और पत्थर के खंभों की प्रशंसा करें।",
                "**मानेक चौक**: देर रात लगने वाले फूड कोर्ट में स्थानीय स्ट्रीट व्यंजनों का स्वाद लें।",
                "**साबरमती रिवरफ्रंट**: नदी के किनारे बने मार्ग पर शाम की आरामदायक सैर का आनंद लें।",
                "**लॉ गार्डन**: रंग-बिरंगे गुजराती हस्तशिल्प बाजार के स्टालों को देखें।",
                "**सीदी सैयद**: ऐतिहासिक पत्थर की नक्काशीदार जालीदार खिड़की की तस्वीर लें।",
                "**सरखेज रोजा**: भव्य मकबरे और प्राचीन झील संरचनाओं का अन्वेषण करें।",
                "**कैलिको संग्रहालय**: भारतीय कपड़ा विरासत के प्रसिद्ध संग्रहालय का दौरा करें।"
            ],
            "te": [
                "**సబర్మతి ఆశ్రమం**: మహాత్మా గాంధీ నివసించిన పవిత్ర ఆశ్రమ ప్రదేశాన్ని సందర్శించండి.",
                "**అదాలజ్ మెట్ల బావి**: అద్భుతమైన రాతి చెక్కడాలు గల మెట్ల బావిని సందర్శించండి.",
                "**మానెక్ చౌక్**: అర్ధరాత్రి పూట లభించే వివిధ రకాల నోరూరించే వంటకాలను ఇక్కడ ఆస్వాదించండి.",
                "**సబర్మతి రివర్‌ఫ్రంట్**: సాయంత్రం నదీ తీరం వెంబడి నడుస్తూ ప్రశాంతంగా గడపండి.",
                "**లా గార్డెన్**: గుజరాతీ హస్తకళల బజార్లలో రంగురంగుల వస్తువుల షాపింగ్ చేయండి.",
                "**సిదీ సయ్యద్ మసీదు**: ఇక్కడి ప్రసిద్ధ రాతి చెక్కడాల కిటికీ అందాలను ఫోటో తీయండి.",
                "**సర్ఖేజ్ రోజా**: అద్భుతమైన చారిత్రక సమాధులు మరియు కోనేరు ఆకృతిని అన్వేషించండి.",
                "**కాలికో మ్యూజియం**: భారతీయ వస్త్రాల చరిత్ర గల ప్రసిద్ధ మ్యూజియాన్ని సందర్శించండి."
            ]
        }
    }
}


CATEGORY_TITLES = {
    "temples": {
        "en": "Spiritual & Temple Exploration",
        "hi": "आध्यात्मिक और मंदिर दर्शन",
        "te": "ఆధ్యాత్మికం & దేవాలయ సందర్శన"
    },
    "nature": {
        "en": "Nature & Scenic Beauty",
        "hi": "प्रकृति और सुंदर दृश्य",
        "te": "ప్రకృతి & ప్రకృతి సౌందర్యం"
    },
    "food": {
        "en": "Culinary Highlights & Local Cuisine",
        "hi": "स्थानीय व्यंजन और स्वाद सफ़र",
        "te": "స్థానిక వంటకాలు & వీధి ఆహారం"
    },
    "shopping": {
        "en": "Arts, Crafts & Local Shopping",
        "hi": "कला, शिल्प और स्थानीय खरीदारी",
        "te": "కళలు, చేనేత & షాపింగ్"
    },
    "history": {
        "en": "Historical Monuments & Heritage",
        "hi": "ऐतिहासिक स्मारक और विरासत",
        "te": "చారిత్రక కట్టడాలు & వారసత్వం"
    },
    "default": {
        "en": "Wonders & Heritage Highlights",
        "hi": "अद्भुत विरासत और स्थल",
        "te": "చారిత్రక అద్భుతాలు & వారసత్వం"
    }
}

MODIFIERS = {
    "en": {
        "temples": [
            {"suffix": " - Evening Aarti & Meditation", "extra": "Return in the evening to witness the beautiful aarti ceremony, participate in silent meditation, and enjoy the peaceful spiritual hymns."},
            {"suffix": " - Architecture & Photography Walk", "extra": "Focus on the intricate carvings and marvelous architecture. Take a guided photography tour around the ancient pillars and courtyards."},
            {"suffix": " - Spiritual Library & Prasad", "extra": "Visit the temple's spiritual museum and library, interact with local scholars, and savor the sanctified temple prasadam."},
            {"suffix": " - Sacred Pond & Surroundings", "extra": "Take a peaceful walk around the sacred temple pond and the surrounding herbal garden pathways."}
        ],
        "nature": [
            {"suffix": " - Sunrise Walk & Yoga", "extra": "Experience the serene atmosphere early in the morning. Practice light yoga and breathing exercises amidst the lush green surroundings."},
            {"suffix": " - Wildlife & Photography Tour", "extra": "Embark on a specialized nature photography trail, spotting local birds and unique flora under the guidance of a nature guide."},
            {"suffix": " - Sunset View & Lake Boating", "extra": "Enjoy a relaxing evening boat ride or walk along the lakeside, watching a spectacular sunset over the water."},
            {"suffix": " - Botanical Trail & Picnic", "extra": "Walk through the hidden garden pathways and have a quiet picnic under the shade of ancient trees."}
        ],
        "food": [
            {"suffix": " - Street Food & Dessert Crawl", "extra": "Explore the bustling street side stalls nearby to savor unique local desserts, sweet drinks, and savory snacks."},
            {"suffix": " - Culinary Workshop & Tasting", "extra": "Attend a live cooking demonstration by local chefs to understand the blend of traditional spices and heritage recipes."},
            {"suffix": " - Traditional Dinner & Local Music", "extra": "Enjoy an authentic sit-down feast accompanied by soft local folk or classical music performances."},
            {"suffix": " - Morning Breakfast & Tea Walk", "extra": "Start early to sample local breakfast delicacies and hot specialty teas at legendary corner shops."}
        ],
        "shopping": [
            {"suffix": " - Artisan Interaction & Weaving", "extra": "Meet the local master artisans, observe their hand-weaving or crafting techniques, and buy customized items directly."},
            {"suffix": " - Antique & Curio Hunt", "extra": "Browse the older sections of the bazaar for unique antique souvenirs, brassware, and traditional decorative pieces."},
            {"suffix": " - Evening Bazaar & Spice Shopping", "extra": "Explore the vibrant night market stalls, purchasing high-quality local spices, handloom fabrics, and handmade jewelry."},
            {"suffix": " - Souvenir Collection & Sweets", "extra": "Collect personalized souvenirs, handicraft keepsakes, and boxes of traditional local sweets for friends and family."}
        ],
        "history": [
            {"suffix": " - Light & Sound Show", "extra": "Attend the magnificent evening light and sound show depicting the rich history and legends of the site."},
            {"suffix": " - Guided Museum Tour", "extra": "Take a deep-dive guided tour of the museum galleries, exploring ancient weaponry, manuscripts, and royal artifacts."},
            {"suffix": " - Hidden Corridors & Architecture Walk", "extra": "Explore the lesser-known pathways, hidden corridors, and vintage architecture with a certified historian."},
            {"suffix": " - Heritage Photography & Sunset", "extra": "Capture stunning wide-angle shots of the monument silhouettes during the golden hour sunset."}
        ],
        "default": [
            {"suffix": " - Local Exploration", "extra": "Take an off-the-beaten-path walk around the local neighborhood, interacting with residents and discovering hidden spots."},
            {"suffix": " - Evening Walk & Street Eats", "extra": "Stroll through the scenic spots during the cool evening hours and relish popular local snacks."},
            {"suffix": " - Cultural Center Visit", "extra": "Visit a local cultural center or art gallery exhibiting regional paintings, sculptures, and heritage relics."},
            {"suffix": " - Farewell Tour & Keepsakes", "extra": "Revisit your favorite scenic viewpoints, pick up remaining keepsakes, and enjoy a traditional dinner."}
        ]
    },
    "hi": {
        "temples": [
            {"suffix": " - संध्या आरती और ध्यान", "extra": "शाम को सुंदर आरती समारोह देखने, मौन ध्यान लगाने और शांतिपूर्ण भजनों का आनंद लेने के लिए वापस आएं।"},
            {"suffix": " - वास्तुकला और फोटोग्राफी वॉक", "extra": "जटिल नक्काशी और अद्भुत वास्तुकला पर ध्यान केंद्रित करें। प्राचीन खंभों और आंगनों के चारों ओर एक निर्देशित फोटोग्राफी यात्रा का आनंद लें।"},
            {"suffix": " - आध्यात्मिक पुस्तकालय और प्रसाद", "extra": "मंदिर के आध्यात्मिक संग्रहालय और पुस्तकालय का दौरा करें, स्थानीय विद्वानों से बातचीत करें और पवित्र मंदिर के प्रसाद का स्वाद लें।"},
            {"suffix": " - पवित्र तालाब और आसपास", "extra": "पवित्र मंदिर के तालाब और आसपास के हर्बल उद्यान मार्गों के चारों ओर एक शांतिपूर्ण सैर करें।"}
        ],
        "nature": [
            {"suffix": " - सूर्योदय वॉक और योग", "extra": "सुबह-सुबह शांत वातावरण का अनुभव करें। हरी-भरी हरियाली के बीच हल्के योग और श्वास क्रियाओं का अभ्यास करें।"},
            {"suffix": " - वन्यजीव और फोटोग्राफी टूर", "extra": "स्थानीय पक्षियों और अनूठी वनस्पतियों को देखने के लिए एक विशेष प्रकृति फोटोग्राफी मार्ग पर चलें।"},
            {"suffix": " - सूर्यास्त दृश्य और नौका विहार", "extra": "झील के किनारे शाम को नाव की सवारी या सैर का आनंद लें, और पानी पर एक शानदार सूर्यास्त देखें।"},
            {"suffix": " - वानस्पतिक मार्ग और पिकनिक", "extra": "उद्यान के छिपे हुए रास्तों पर चलें और प्राचीन पेड़ों की छाया में एक शांत पिकनिक का आनंद लें।"}
        ],
        "food": [
            {"suffix": " - स्ट्रीट फूड और मिठाई सफ़र", "extra": "अनोखे स्थानीय डेसर्ट, मीठे पेय और नमकीन स्नैक्स का स्वाद लेने के लिए आस-पास के हलचल भरे स्ट्रीट स्टालों का अन्वेषण करें।"},
            {"suffix": " - पाक कला कार्यशाला और स्वाद", "extra": "पारंपरिक मसालों और विरासत व्यंजनों के मिश्रण को समझने के लिए स्थानीय रसोइयों द्वारा लाइव कुकिंग प्रदर्शन में भाग लें।"},
            {"suffix": " - पारंपरिक रात्रिभोज और संगीत", "extra": "स्थानीय लोक या शास्त्रीय संगीत प्रदर्शन के साथ एक प्रामाणिक पारंपरिक दावत का आनंद लें।"},
            {"suffix": " - सुबह का नाश्ता और चाय यात्रा", "extra": "प्रसिद्ध कोनों की दुकानों पर स्थानीय नाश्ते के व्यंजनों और गर्म चाय के स्वाद के साथ दिन की शुरुआत करें।"}
        ],
        "shopping": [
            {"suffix": " - शिल्पकार संवाद और बुनाई", "extra": "स्थानीय शिल्पकारों से मिलें, उनकी बुनाई या क्राफ्टिंग तकनीकों को देखें और सीधे हस्तनिर्मित वस्तुएं खरीदें।"},
            {"suffix": " - प्राचीन और कलाकृतियों की खोज", "extra": "अनोखे प्राचीन स्मृति चिन्ह, पीतल के बर्तन और पारंपरिक सजावटी सामानों के लिए बाजार के पुराने हिस्सों को देखें।"},
            {"suffix": " - शाम का बाजार और मसाला खरीदारी", "extra": "जीवंत रात के बाजारों का भ्रमण करें, उच्च गुणवत्ता वाले स्थानीय मसाले, हथकरघा कपड़े और हस्तनिर्मित गहने खरीदें।"},
            {"suffix": " - स्मृति चिन्ह और मिठाई संग्रह", "extra": "दोस्तों और परिवार के लिए व्यक्तिगत स्मृति चिन्ह, हस्तकला उपहार और पारंपरिक स्थानीय मिठाइयों के डिब्बे खरीदें।"}
        ],
        "history": [
            {"suffix": " - लाइट एंड साउंड शो", "extra": "इस ऐतिहासिक स्थल के समृद्ध इतिहास और किंवदंतियों को दर्शाने वाले शानदार शाम के लाइट एंड साउंड शो में भाग लें।"},
            {"suffix": " - निर्देशित संग्रहालय यात्रा", "extra": "संग्रहालय दीर्घाओं का विस्तृत दौरा करें, और प्राचीन हथियारों, पांडुलिपियों तथा शाही कलाकृतियों का अन्वेषण करें।"},
            {"suffix": " - छिपे हुए गलियारे और वास्तुकला", "extra": "एक प्रमाणित इतिहासकार के साथ कम प्रसिद्ध मार्गों, छिपे हुए गलियारों और पुरानी वास्तुकला का पता लगाएं।"},
            {"suffix": " - विरासत फोटोग्राफी और सूर्यास्त", "extra": "सुनहरे सूर्यास्त के समय ऐतिहासिक स्मारक की सुंदर तस्वीरें अपने कैमरे में कैद करें।"}
        ],
        "default": [
            {"suffix": " - स्थानीय अन्वेषण", "extra": "स्थानीय पड़ोस के चारों ओर एक अनोखी सैर करें, निवासियों के साथ बातचीत करें और छिपे हुए स्थानों की खोज करें।"},
            {"suffix": " - शाम की सैर और स्ट्रीट फूड", "extra": "शाम के ठंडे घंटों के दौरान सुंदर स्थानों पर टहलें और लोकप्रिय स्थानीय स्नैक्स का आनंद लें।"},
            {"suffix": " - सांस्कृतिक केंद्र का दौरा", "extra": "क्षेत्रीय चित्रों, मूर्तियों और विरासत के अवशेषों को प्रदर्शित करने वाले एक स्थानीय सांस्कृतिक केंद्र या कला दीर्घा का दौरा करें।"},
            {"suffix": " - विदारी यात्रा और स्मृति चिन्ह", "extra": "अपने पसंदीदा दृश्यों को फिर से देखें, शेष उपहार खरीदें और एक पारंपरिक विदारी रात्रिभोज का आनंद लें।"}
        ]
    },
    "te": {
        "temples": [
            {"suffix": " - సాయంత్రం హారతి & ధ్యానం", "extra": "సాయంత్రం వేళ జరిగే సుందరమైన హారతి సేవను వీక్షించడానికి, ప్రశాంతమైన ధ్యానంలో పాల్గొనడానికి మరియు ఆధ్యాత్మిక కీర్తనలను వినడానికి తిరిగి ఆలయాన్ని సందర్శించండి."},
            {"suffix": " - శిల్పకళ & ఫోటోగ్రఫీ విహారం", "extra": "ఆలయంలోని అద్భుతమైన శిల్పకళ మరియు నగిషీలపై దృష్టి పెట్టండి. పురాతన స్తంభాలు మరియు ప్రాంగణాల చుట్టూ ఫోటోగ్రఫీ చేయండి."},
            {"suffix": " - ఆధ్యాత్మిక గ్రంథాలయం & ప్రసాదం", "extra": "ఆలయంలోని ఆధ్యాత్మిక మ్యూజియం మరియు గ్రంథాలయాన్ని సందర్శించి, పండితులతో మాట్లాడి, పవిత్రమైన ఆలయ ప్రసాదాన్ని స్వీకరించండి."},
            {"suffix": " - పవిత్ర కోనేరు & పరిసరాలు", "extra": "ఆలయ పవిత్ర కోనేరు మరియు దాని చుట్టూ ఉన్న మూలికా వన మార్గాల గుండా ప్రశాంతమైన నడకను ఆస్వాదించండి."}
        ],
        "nature": [
            {"suffix": " - సూర్యోదయ నడక & యోగా", "extra": "ఉదయాన్నే ప్రశాంతమైన వాతావరణాన్ని అనుభవించండి. పచ్చని ప్రకృతి మధ్య తేలికపాటి యోగా మరియు శ్వాస వ్యాయామాలు చేయండి."},
            {"suffix": " - వన్యప్రాణుల & ఫోటోగ్రఫీ టూర్", "extra": "స్థానిక పక్షులు మరియు విలక్షణమైన వృక్షజాలాన్ని గమనించడానికి ప్రత్యేక ప్రకృతి ఫోటోగ్రఫీ ట్రయల్‌ను అనుసరించండి."},
            {"suffix": " - సూర్యాస్తమయ వీక్షణం & బోటింగ్", "extra": "సరస్సుపై సూర్యాస్తమయాన్ని వీక్షిస్తూ, సాయంత్రం వేళ ప్రశాంతమైన బోట్ ప్రయాణం లేదా సరస్సు గట్టు వెంబడి నడకను ఆస్వాదించండి."},
            {"suffix": " - వృక్షశాస్త్ర మార్గం & పిక్నిక్", "extra": "తోటలోని నిగూఢ మార్గాల గుండా నడుస్తూ, పురాతన వృక్షాల నీడలో ప్రశాంతమైన పిక్నిక్‌ను ఆస్వాదించండి."}
        ],
        "food": [
            {"suffix": " - వీధి ఆహారం & స్వీట్ల రుచులు", "extra": "సమీపంలోని సందడిగల వీధి స్టాల్స్‌ను సందర్శించి, ప్రత్యేకమైన స్థానిక స్వీట్లు, పానీయాలు మరియు కారంగా ఉండే వంటకాలను రుచి చూడండి."},
            {"suffix": " - వంటకాల వర్క్‌షాప్ & రుచి పరీక్ష", "extra": "స్థానిక చెఫ్‌లచే నిర్వహించబడే వంటల తయారీ విధానాన్ని చూసి, సాంప్రదాయ మసాలాలు మరియు వంటకాల రహస్యాలను తెలుసుకోండి."},
            {"suffix": " - సాంప్రదాయ విందు & స్థానిక సంగీతం", "extra": "స్థానిక జానపద లేదా శాస్త్రీय సంగీత కచేరీల మధ్య సాంప్రదాయ విందును ఆస్వాదించండి."},
            {"suffix": " - ఉదయపు అల్పాహారం & టీ విహారం", "extra": "ప్రసిద్ధ స్థానిక తినుబండారాల వద్ద వేడివేడి అల్పాహారాలు మరియు టీ రుచులతో రోజును ప్రారంభించండి."}
        ],
        "shopping": [
            {"suffix": " - చేతివృత్తుల కళాకారులతో సంభాషణ", "extra": "స్థానిక కళాకారులను కలుసుకుని, వారి చేనేత లేదా హస్తకళల నైపుణ్యాలను గమనించండి మరియు నేరుగా వారి వద్ద నుండే కొనుగోలు చేయండి."},
            {"suffix": " - పురాతన వస్తువుల సేకరణ", "extra": "అరుదైన పురాతన వస్తువులు, ఇత్తడి కళాఖండాలు మరియు సాంప్రదాయ అలంకరణ వస్తువుల కోసం బజార్‌లోని పాత వీధులను అన్వేషించండి."},
            {"suffix": " - సాయంత్రం బజార్ & మసాలా దినుసులు", "extra": "రాత్రి పూట సందడిగా ఉండే మార్కెట్లను సందర్శించి, నాణ్యమైన స్థానిక మసాలా దినుసులు, చేనేత వస్త్రాలు మరియు హస్తకళల ఆభరణాలను కొనుగోలు చేయండి."},
            {"suffix": " - జ్ఞాపికలు & స్వీట్ల కొనుగోలు", "extra": "కుటుంబ సభ్యులు మరియు స్నేహితుల కోసం స్థానిక హస్తకళల జ్ఞాపికలను మరియు సాంప్రదాయ స్వీట్ బాక్సులను కొనుగోలు చేయండి."}
        ],
        "history": [
            {"suffix": " - లైట్ అండ్ సౌండ్ షో", "extra": "ఈ చారిత్రక ప్రదేశం యొక్క వైభవాన్ని మరియు కథలను వివరించే అద్భుతమైన సాయంత్రం లైట్ అండ్ సౌండ్ షోను తిలకించండి."},
            {"suffix": " - మ్యూజియం గైడెడ్ టూర్", "extra": "మ్యూజియం గ్యాలరీలను సందర్శించి, పురాతన ఆయుధాలు, తాళపత్ర గ్రంథాలు మరియు రాజవంశపు కళాఖండాల గురించి గైడ్ ద్వారా తెలుసుకోండి."},
            {"suffix": " - నిగూఢ మార్గాలు & శిల్పకళా శైలి", "extra": "చరిత్రకారునితో కలిసి ఈ కట్టడాలలోని రహస్య మార్గాలు, తక్కువ ప్రసిద్ధి చెందిన గదులు మరియు పురాతన నిర్మాణ శైలిని అన్వేషించండి."},
            {"suffix": " - చారిత్రక ఫోటోగ్రఫీ & సూర్యాస్తమయం", "extra": "గోల్డెన్ అవర్ సూర్యాస్తమయ సమయంలో ఈ చారిత్రక కట్టడం యొక్క అద్భుతమైన ఛాయాచిత్రాలను తీయండి."}
        ],
        "default": [
            {"suffix": " - స్థానిక అన్వేషణ", "extra": "సమీప స్థానిక పరిసరాలలో నడుస్తూ, అక్కడి ప్రజల జీవనశైలిని గమనించండి మరియు తక్కువగా ప్రసిద్ధి చెందిన ప్రదేశాలను కనుగొనండి."},
            {"suffix": " - సాయంత్రం విహారం & స్థానిక తినుబండారాలు", "extra": "సాయంత్రపు ఆహ్లాదకరమైన వాతావరణంలో ప్రముఖ వీధులలో విహరిస్తూ, స్థానిక ప్రత్యేక తినుబండారాలను ఆస్వాదించండి."},
            {"suffix": " - సాంస్కృతిక కేంద్ర సందర్శన", "extra": "ప్రాంతీయ చిత్రలేఖనాలు, శిల్పాలు మరియు సాంస్కృతిక విశేషాలను ప్రదర్శించే స్థానిక సాంస్కృతిక కేంద్రం లేదా ఆర్ట్ గ్యాలరీని సందర్శించండి."},
            {"suffix": " - ముగింపు పర్యటన & జ్ఞాపికలు", "extra": "మీకు బాగా నచ్చిన ప్రదేశాలను మరొక్కసారి సందర్శించి, మిగిలిన జ్ఞాపికలను కొనుగోలు చేసి సాంప్రదాయ వీడ్కోలు విందుతో ముగించండి."}
        ]
    }
}

def get_response(query, city, language, provider, api_key=None):
    """
    TravelSathi API Interface.
    Attempts to route queries to the real RAG AI backend.
    If the backend is not configured or fails, falls back to a multilingual dynamic mock.
    
    Arguments:
        query (str): The prompt, planner, or festival question.
        city (str): Selected destination (e.g. Hyderabad, Varanasi, Jaipur).
        language (str): Target translation language (en, te, hi).
        provider (str): AI provider selected (Gemini, Ollama, OpenAI).
        api_key (str): Optional API key.
        
    Returns:
        dict: {
            "answer": str (itinerary or festival explanation),
            "phrases": list (useful local phrases),
            "budget": dict (category-wise percentage breakdown)
        }
    """
    # 1. Attempt to call real backend first if available and provider is not a Mock option
    if HAS_BACKEND and provider.lower() not in ["mock", "offline", "offline mock"]:
        lang_map_full = {
            "en": "English",
            "te": "Telugu",
            "hi": "Hindi"
        }
        backend_lang = lang_map_full.get(language, language)
        try:
            # Quick check to avoid long timeout if API keys are missing for API-based models
            provider_lower = provider.lower()
            if provider_lower == "groq" and not api_key:
                raise ValueError("Missing Groq API key")
            elif provider_lower == "openrouter" and not api_key:
                raise ValueError("Missing OpenRouter API key")
            elif provider_lower == "gemini" and not api_key and not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
                raise ValueError("Missing Gemini API key")
                
            res = get_backend_response(
                query=query,
                city=city,
                language=backend_lang,
                provider=provider,
                api_key=api_key
            )
            if res and isinstance(res, dict) and "answer" in res:
                logger.info(f"Successfully generated response using backend AI ({provider}).")
                return res
        except Exception as e:
            logger.warning(f"Backend AI ({provider}) failed or is not configured. Falling back to dynamic mock. Error: {str(e)}")

    # 2. Dynamic Mock Fallback Implementation
    city_str = str(city).lower()
    
    # Check if city name matches (supporting multiple languages)
    is_hyd = "hyderabad" in city_str or "హైదరాబాద్" in city_str or "हैदराबाद" in city_str
    is_var = "varanasi" in city_str or "వారణాసి" in city_str or "वाराणसी" in city_str
    is_jai = "jaipur" in city_str or "జైపూర్" in city_str or "जयपुर" in city_str
    is_mum = "mumbai" in city_str or "ముంబై" in city_str or "मुंबई" in city_str
    is_kol = "kolkata" in city_str or "కోల్‌కతా" in city_str or "कोलकाता" in city_str
    is_del = "delhi" in city_str or "ఢిల్లీ" in city_str or "दिल्ली" in city_str
    is_che = "chennai" in city_str or "చెన్నై" in city_str or "चेन्नई" in city_str
    is_ahm = "ahmedabad" in city_str or "అహ్మదాబాద్" in city_str or "अहमदाबाद" in city_str
    
    if is_hyd:
        city_name_local = "హైదరాబాద్" if language == "te" else ("हैदराबाद" if language == "hi" else "Hyderabad")
    elif is_var:
        city_name_local = "వారణాసి" if language == "te" else ("वाराणसी" if language == "hi" else "Varanasi")
    elif is_jai:
        city_name_local = "జైపూర్" if language == "te" else ("जयपुर" if language == "hi" else "Jaipur")
    elif is_mum:
        city_name_local = "ముంబై" if language == "te" else ("मुंबई" if language == "hi" else "Mumbai")
    elif is_kol:
        city_name_local = "కోల్‌కతా" if language == "te" else ("कोलकाता" if language == "hi" else "Kolkata")
    elif is_del:
        city_name_local = "ఢిల్లీ" if language == "te" else ("दिल्ली" if language == "hi" else "Delhi")
    elif is_che:
        city_name_local = "చెన్నై" if language == "te" else ("चेन्नई" if language == "hi" else "Chennai")
    elif is_ahm:
        city_name_local = "అహ్మదాబాద్" if language == "te" else ("अहमदाबाद" if language == "hi" else "Ahmedabad")
    else:
        city_name_local = city

    # Determine if it's a festival query or itinerary query
    is_festival_query = "festival" in query.lower() or "పండుగ" in query.lower() or "त्योहार" in query.lower()
    
    # A. Handle festival queries
    if is_festival_query:
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
            
    # B. Handle itinerary queries with custom interest detection
    else:
        # Detect interests from query/interests string
        interests_str = ""
        if "interests:" in query.lower():
            interests_str = query.lower().split("interests:")[-1].strip()
        else:
            interests_str = query.lower()
            
        has_temples = any(k in interests_str for k in ["temple", "spiritual", "religious", "puja", "worship", "god", "shiva", "kali", "aarti", "గుడి", "దేవాలయం", "పూజ", "मंदिर", "पूजा"])
        has_food = any(k in interests_str for k in ["food", "street food", "streetfood", "cuisine", "dining", "biryani", "lassi", "kachori", "ghevar", "gatte", "curry", "రుచులు", "ఆహారం", "బిర్యానీ", "भोजन", "खाना", "बिरयानी", "कचौड़ी"])
        has_shopping = any(k in interests_str for k in ["shop", "market", "bazaar", "craft", "weav", "saree", "bangle", "handicraft", "సరిహద్దు", "బజార్", "షాపింగ్", "చేనేత", "खरीदारी", "बाजार", "साड़ी"])
        has_nature = any(k in interests_str for k in ["nature", "park", "garden", "lake", "scenic", "beautiful", "beach", "hill", "mountain", "ప్రకృతి", "పార్కు", "చెరువు", "प्रकृति", "पार्क", "झील"])
        has_history =  any(k in interests_str for k in ["museum", "history", "heritage", "fort", "palace", "monument", "charminar", "golconda", "amer", "hawa", "చరిత్ర", "కోట", "మ్యూజియం", "ఇతిహాసం", "इतिहास", "किला", "महल", "संग्रहालय"])
        
        detected = []
        if has_temples:
            detected.append("temples")
        if has_food:
            detected.append("food")
        if has_shopping:
            detected.append("shopping")
        if has_nature:
            detected.append("nature")
        if has_history:
            detected.append("history")

        city_key = "hyderabad"
        if is_hyd:
            city_key = "hyderabad"
        elif is_var:
            city_key = "varanasi"
        elif is_jai:
            city_key = "jaipur"
        elif is_mum:
            city_key = "mumbai"
        elif is_kol:
            city_key = "kolkata"
        elif is_del:
            city_key = "delhi"
        elif is_che:
            city_key = "chennai"
        elif is_ahm:
            city_key = "ahmedabad"

        # Determine all categories supported by the city
        all_cats = ["history", "nature", "temples", "food", "shopping", "default"]
        supported_cats = [c for c in all_cats if c in ITINERARIES[city_key]]

        if not detected or detected == ["default"]:
            # Default to the 'default' category to show primary attractions
            detected = ["default"]
        else:
            # User specified interests. Filter them to supported ones first
            detected = [c for c in detected if c in supported_cats]
            if not detected:
                detected = ["default"]

        import re
        days_match = re.search(r"Generate (\d+)-day itinerary", query, re.IGNORECASE)
        num_days = 3
        if days_match:
            num_days = int(days_match.group(1))

        # Build cyclical list of detected categories based on num_days
        day_categories_extended = []
        for i in range(num_days):
            day_categories_extended.append(detected[i % len(detected)])
            
        lang_key = language if language in ["en", "te", "hi"] else "en"
        
        answer_lines = []
        if lang_key == "hi":
            answer_lines.append(f"### 🗺️ AI-जनित यात्रा कार्यक्रम: **{city_name_local}** (प्रदाता: {provider} - Fallback)\n")
            answer_lines.append(f"यहाँ आपकी प्राथमिकताओं के आधार पर तैयार किया गया यात्रा कार्यक्रम है:\n")
        elif lang_key == "te":
            answer_lines.append(f"### 🗺️ AI సృష్టించిన ప్రయాణ ప్రణాళిక: **{city_name_local}** (ప్రొవైడర్: {provider} - Fallback)\n")
            answer_lines.append(f"మీ ప్రాధాన్యతలకు అనుగుణంగా రూపొందించబడిన ప్రయాణ ప్రణాళిక ఇక్కడ ఉంది:\n")
        else:
            answer_lines.append(f"### 🗺️ AI-Generated Itinerary for **{city_name_local}** (Provider: {provider} - Fallback)\n")
            answer_lines.append(f"Here is a curated itinerary tailored for you:\n")
            
        emoji_cycle = ["🌅", "🎨", "🛍️", "🚶", "📸", "🎭", "🚢", "🍽️"]

        for d in range(num_days):
            cat = day_categories_extended[d]
            cat_name = CATEGORY_TITLES[cat][lang_key]
            
            items = ITINERARIES[city_key][cat][lang_key]
            content = items[d % len(items)]
            
            # Modify content dynamically if repeating the items
            run_number = (d // len(items)) - 1
            if run_number >= 0:
                import re
                match = re.match(r"\*\*(.*?)\*\*:\s*(.*)", content)
                if match:
                    title = match.group(1)
                    desc = match.group(2)
                    
                    cat_mods = MODIFIERS[lang_key].get(cat, MODIFIERS[lang_key]["default"])
                    mod = cat_mods[d % len(cat_mods)]
                    
                    modified_title = f"{title}{mod['suffix']}"
                    modified_desc = f"{desc} {mod['extra']}"
                    content = f"**{modified_title}**: {modified_desc}"
            
            emo = emoji_cycle[d % len(emoji_cycle)]
            if lang_key == "hi":
                answer_lines.append(f"#### {emo} दिन {d+1}: {cat_name}\n- {content}\n")
            elif lang_key == "te":
                answer_lines.append(f"#### {emo} రోజు {d+1}: {cat_name}\n- {content}\n")
            else:
                answer_lines.append(f"#### {emo} Day {d+1}: {cat_name}\n- {content}\n")

        answer = "\n".join(answer_lines)

    # 3. Local phrase assistant based on selected city
    is_translation = query.startswith("TRANSLATE_PHRASE:")
    phrase_to_translate = query.replace("TRANSLATE_PHRASE:", "").strip() if is_translation else ""

    if is_translation:
        # Normalize custom phrase
        norm_phrase = phrase_to_translate.lower().strip("?.! ")
        
        # Simple word map for Telugu, Hindi, Marathi, Bengali, Tamil, Gujarati
        dict_translations = {
            "hello": {
                "te": ("నమస్కారం", "Namaskaram"),
                "hi": ("नमस्ते", "Namaste"),
                "mr": ("नमस्कार", "Namaskar"),
                "bn": ("নমস্কার", "Nomoshkar"),
                "ta": ("வணக்கம்", "Vanakkam"),
                "gu": ("નમસ્તે", "Namaste")
            },
            "thank you": {
                "te": ("ధన్యవాదాలు", "Dhanyavadalu"),
                "hi": ("धन्यवाद", "Dhanyavaad"),
                "mr": ("धन्यवाद", "Dhanyawad"),
                "bn": ("ধন্যবাদ", "Dhonnobad"),
                "ta": ("நன்றி", "Nandri"),
                "gu": ("આભાર", "Aabhar")
            },
            "thanks": {
                "te": ("ధన్యవాదాలు", "Dhanyavadalu"),
                "hi": ("धन्यवाद", "Dhanyavaad"),
                "mr": ("धन्यवाद", "Dhanyawad"),
                "bn": ("ধন্যবাদ", "Dhonnobad"),
                "ta": ("நன்றி", "Nandri"),
                "gu": ("આભાર", "Aabhar")
            },
            "how are you": {
                "te": ("ఎలా ఉన్నారు?", "Ela unnaru?"),
                "hi": ("आप कैसे हैं?", "Aap kaise hain?"),
                "mr": ("कसे आहात?", "Kase aahat?"),
                "bn": ("কেমন আছেন?", "Kemon achen?"),
                "ta": ("எப்படி இருக்கிறீர்கள்?", "Eppadi irukkireergal?"),
                "gu": ("કેમ છો?", "Kem cho?")
            },
            "where is": {
                "te": ("ఎక్కడ ఉంది?", "Ekkada undi?"),
                "hi": ("कहाँ है?", "Kahan hai?"),
                "mr": ("कुठे आहे?", "Kuthe aahe?"),
                "bn": ("কোথায়?", "Kothay?"),
                "ta": ("எங்கே இருக்கிறது?", "Enge irukkirathu?"),
                "gu": ("ક્યાં છે?", "Kyan chhe?")
            }
        }
        
        # Determine target language code based on target city
        if is_hyd:
            target_lang_code = "te"
            lang_label = "Telugu"
        elif is_var or is_jai or is_del:
            target_lang_code = "hi"
            lang_label = "Hindi"
        elif is_mum:
            target_lang_code = "mr"
            lang_label = "Marathi"
        elif is_kol:
            target_lang_code = "bn"
            lang_label = "Bengali"
        elif is_che:
            target_lang_code = "ta"
            lang_label = "Tamil"
        elif is_ahm:
            target_lang_code = "gu"
            lang_label = "Gujarati"
        else:
            target_lang_code = "hi"
            lang_label = "Hindi"
            
        translation_val = None
        pronunciation_val = "N/A"
        
        # Match common phrases
        for key, lang_map in dict_translations.items():
            if key in norm_phrase:
                translation_val, pronunciation_val = lang_map.get(target_lang_code, ("N/A", "N/A"))
                break
                
        # If no match, generate a dynamic mock translation
        if not translation_val:
            translation_val = f"(Offline) {phrase_to_translate} in {lang_label} script"
            pronunciation_val = "N/A"
            
        phrases = [{"phrase": phrase_to_translate, "translation": translation_val, "pronunciation": pronunciation_val}]
    elif is_hyd:
        if is_translation:
            phrases = [{"phrase": phrase_to_translate, "translation": "(Offline Translation Unavailable)", "pronunciation": "N/A"}]
        else:
            phrases = [
                {"phrase": "Hello / Good morning", "translation": "నమస్కారం (Namaskaram)", "pronunciation": "Nah-mah-skah-rum"},
            {"phrase": "How much is this?", "translation": "ఇది ఎంత? (Idi entha?)", "pronunciation": "Ee-dee en-tah?"},
            {"phrase": "Where is Charminar?", "translation": "చార్మినార్ ఎక్కడ ఉంది? (Charminar ekkada undi?)", "pronunciation": "Char-mee-nar ek-kah-dah oon-dee?"},
            {"phrase": "The food is delicious!", "translation": "ఆహారం చాలా రుచిగా ఉంది! (Aaharam chala ruchiga undi!)", "pronunciation": "Aa-haa-rum chaa-lah roo-chee-gah oon-dee"},
            {"phrase": "Thank you", "translation": "ధన్యవాదాలు (Dhanyavadalu)", "pronunciation": "Dhun-yah-vah-dah-loo"}
        ]
    elif is_var:
        if is_translation:
            phrases = [{"phrase": phrase_to_translate, "translation": "(Offline Translation Unavailable)", "pronunciation": "N/A"}]
        else:
            phrases = [
                {"phrase": "Hello / Greetings", "translation": "नमस्ते (Namaste) / प्रणाम (Pranam)", "pronunciation": "Nah-muh-stay / Pruh-naam"},
                {"phrase": "Where is the Dashashwamedh Ghat?", "translation": "दशाश्वमेध घाट कहाँ है? (Dashashwamedh Ghat kahan hai?)", "pronunciation": "Duh-shaash-wuh-maydh Ghaat kuh-haan hai?"},
                {"phrase": "How much is this boat ride?", "translation": "नाव की सवारी का कितना हुआ? (Naav ki sawari ka kitna hua?)", "pronunciation": "Naav kee suh-waa-ree kaa kit-naa hoo-aa?"},
                {"phrase": "I want a cup of tea", "translation": "मुझे एक कप चाय चाहिए (Mujhe ek cup chai chahiye)", "pronunciation": "Moo-jhay ek cup chaai chaa-hee-ye"},
                {"phrase": "Thank you", "translation": "धन्यवाद (Dhanyavaad)", "pronunciation": "Dhun-yuh-vaad"}
            ]
    elif is_jai:
        if is_translation:
            phrases = [{"phrase": phrase_to_translate, "translation": "(Offline Translation Unavailable)", "pronunciation": "N/A"}]
        else:
            phrases = [
                {"phrase": "Hello / Welcome", "translation": "खम्मा घणी (Khamma Ghani)", "pronunciation": "Khum-mah Ghuh-nee"},
                {"phrase": "How are you?", "translation": "आप क्यां हो? (Aap kyaan ho?)", "pronunciation": "Aap kyaan ho?"},
                {"phrase": "Where is Hawa Mahal?", "translation": "हवा महल कहाँ है? (Hawa Mahal kahan hai?)", "pronunciation": "Huh-waa Muh-hul kuh-haan hai?"},
                {"phrase": "Very beautiful", "translation": "घणो चोखो (Ghano Chokho)", "pronunciation": "Ghuh-no Cho-kho"},
                {"phrase": "Thank you", "translation": "धन्यवाद (Dhanyavaad)", "pronunciation": "Dhun-yuh-vaad"}
            ]
    elif is_mum:
        if is_translation:
            phrases = [{"phrase": phrase_to_translate, "translation": "(Offline Translation Unavailable)", "pronunciation": "N/A"}]
        else:
            phrases = [
                {"phrase": "Hello", "translation": "नमस्कार (Namaskar)", "pronunciation": "Nah-mus-kar"},
                {"phrase": "How are you?", "translation": "कसे आहात? (Kase aahat?)", "pronunciation": "Kah-say ah-haat?"},
                {"phrase": "Thank you", "translation": "धन्यवाद (Dhanyawad)", "pronunciation": "Dhun-yah-waad"}
            ]
    elif is_kol:
        if is_translation:
            phrases = [{"phrase": phrase_to_translate, "translation": "(Offline Translation Unavailable)", "pronunciation": "N/A"}]
        else:
            phrases = [
                {"phrase": "Hello", "translation": "নমস্কার (Nomoshkar)", "pronunciation": "No-mosh-kar"},
                {"phrase": "How are you?", "translation": "কেমন আছেন? (Kemon achen?)", "pronunciation": "Kay-mon ah-chen?"},
                {"phrase": "Thank you", "translation": "ধন্যবাদ (Dhonnobad)", "pronunciation": "Dhon-no-baad"}
            ]
    elif is_che:
        if is_translation:
            phrases = [{"phrase": phrase_to_translate, "translation": "(Offline Translation Unavailable)", "pronunciation": "N/A"}]
        else:
            phrases = [
                {"phrase": "Hello", "translation": "வணக்கம் (Vanakkam)", "pronunciation": "Vah-nah-kum"},
                {"phrase": "How are you?", "translation": "எப்படி இருக்கிறீர்கள்? (Eppadi irukkireergal?)", "pronunciation": "Ep-pah-dee ee-roo-kee-reer-gal?"},
                {"phrase": "Thank you", "translation": "நன்றி (Nandri)", "pronunciation": "Nun-dree"}
            ]
    elif is_ahm:
        if is_translation:
            phrases = [{"phrase": phrase_to_translate, "translation": "(Offline Translation Unavailable)", "pronunciation": "N/A"}]
        else:
            phrases = [
                {"phrase": "Hello", "translation": "નમસ્તે (Namaste)", "pronunciation": "Nah-mus-tay"},
                {"phrase": "How are you?", "translation": "કેમ છો? (Kem cho?)", "pronunciation": "Kem cho?"},
                {"phrase": "Thank you", "translation": "આભાર (Aabhar)", "pronunciation": "Aa-bhaar"}
            ]
    else:
        if is_translation:
            phrases = [{"phrase": phrase_to_translate, "translation": "(Offline Translation Unavailable)", "pronunciation": "N/A"}]
        else:
            phrases = [
                {"phrase": "Hello", "translation": "नमस्ते (Namaste) / నమస్కారం (Namaskaram)", "pronunciation": "Nah-muh-stay / Nah-mah-skah-rum"},
                {"phrase": "Thank you", "translation": "धन्यवाद (Dhanyavaad) / ధన్యవాదాలు (Dhanyavadalu)", "pronunciation": "Dhun-yuh-vaad / Dhun-yah-vah-dah-loo"}
            ]

    # 4. Dynamic budget allocation based on interests and query budget
    import re
    budget_match = re.search(r"budget of (\d+) INR", query, re.IGNORECASE)
    total_budget = 15000 # default if not found
    if budget_match:
        total_budget = int(budget_match.group(1))

    base_accomm_pct = 40
    base_food_pct = 25
    base_transport_pct = 15
    base_sightseeing_pct = 12
    base_misc_pct = 8
    
    # Customize based on keywords
    if not is_festival_query:
        if has_shopping:
            base_misc_pct = 25
            base_accomm_pct = 30
            base_sightseeing_pct = 5
        elif has_food:
            base_food_pct = 40
            base_accomm_pct = 30
            base_transport_pct = 10
        elif has_temples:
            base_sightseeing_pct = 25
            base_misc_pct = 5
            base_food_pct = 20
            base_accomm_pct = 35

    # Convert percentages to actual amounts (return raw percentages for unit test compatibility and frontend dynamic scaling)
    base_accomm = base_accomm_pct
    base_food = base_food_pct
    base_transport = base_transport_pct
    base_sightseeing = base_sightseeing_pct
    base_misc = base_misc_pct

    if language == "hi":
        budget = {
            "आवास (Accommodation) 🏨": base_accomm,
            "भोजन (Food & Dining) 🍽️": base_food,
            "स्थानीय परिवहन (Local Transport) 🛺": base_transport,
            "दर्शनीय स्थल (Sightseeing) 🎟️": base_sightseeing,
            "विविध (Miscellaneous) 🛍️": base_misc
        }
    elif language == "te":
        budget = {
            "వసతి (Accommodation) 🏨": base_accomm,
            "భోజనం (Food & Dining) 🍽️": base_food,
            "స్థానిక రవాణా (Local Transport) 🛺": base_transport,
            "సందర్శన రుసుములు (Sightseeing) 🎟️": base_sightseeing,
            "ఇతర ఖర్చులు (Miscellaneous) 🛍️": base_misc
        }
    else:
        budget = {
            "Accommodation 🏨": base_accomm,
            "Food & Dining 🍽️": base_food,
            "Local Transport 🛺": base_transport,
            "Sightseeing 🎟️": base_sightseeing,
            "Miscellaneous 🛍️": base_misc
        }

    return {
        "answer": answer,
        "phrases": phrases,
        "budget": budget
    }

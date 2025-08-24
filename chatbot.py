# chatbot.py
from flask import Flask, request, jsonify, render_template
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Chatbot:
    def __init__(self):
        self.responses = [
        {"keywords": ["mastitis", "define", "definition"], "response": "Mastitis is a disease that causes inflammation of the mammary gland in cows, commonly due to bacterial infections."},
        {"keywords": ["symptoms", "signs"], "response": "Common symptoms include udder swelling, redness, heat, pain, fever, and abnormal milk production."},
        {"keywords": ["early", "signs", "initial", "symptoms"], "response": "Early signs of mastitis include slight swelling of the udder, reduced milk yield, and mild pain during milking."},
        {"keywords": ["prevent", "prevention", "avoid"], "response": "Prevention strategies include proper hygiene, clean milking techniques, regular health checks, and avoiding udder injuries."},
        {"keywords": ["hygiene", "cleaning", "sanitize", "equipment"], "response": "Good hygiene practices like cleaning udders, sanitizing milking equipment, and using post-milking teat dips can prevent mastitis."},
        {"keywords": ["milking", "techniques", "proper", "manual", "machine"], "response": "Using proper milking techniques, such as gentle hand milking and clean machinery, helps prevent mastitis."},
        {"keywords": ["types"], "response": "There are two types of mastitis: clinical mastitis, with visible symptoms, and subclinical mastitis, which has no obvious signs but affects milk quality."},
        {"keywords": ["clinical mastitis"], "response": "Clinical mastitis causes visible symptoms such as udder swelling, redness, fever, and clots in the milk."},
        {"keywords": ["subclinical mastitis"], "response": "Subclinical mastitis has no visible symptoms but can be identified through milk tests showing increased somatic cell counts."},
        {"keywords": ["causes", "reason"], "response": "Mastitis is caused by bacteria entering through the teat canal, often due to poor hygiene, injuries, or environmental stress."},
        {"keywords": ["bacteria", "pathogens", "infection"], "response": "The main bacteria causing mastitis are Staphylococcus aureus, Streptococcus agalactiae, and Escherichia coli."},
        {"keywords": ["risk", "factors", "high", "causes"], "response": "Risk factors include poor hygiene, contaminated bedding, improper milking practices, overcrowding, and udder injuries."},
        {"keywords": ["stress", "environment", "overcrowding", "injury"], "response": "Environmental stress, overcrowding, and physical injuries to the udder can increase the risk of mastitis in cows."},
        {"keywords": ["diagnosis", "detect", "test", "somatic cell count"], "response": "Mastitis can be diagnosed through physical examination, milk changes, somatic cell count (SCC), and bacterial cultures."},
        {"keywords": ["milk", "testing", "cell", "count"], "response": "Somatic cell count tests and bacterial cultures are common methods for identifying subclinical mastitis."},
        {"keywords": ["milk", "quality", "safety", "drop", "clots"], "response": "Mastitis reduces milk quality, resulting in clots, discoloration, abnormal consistency, and decreased production."},
        {"keywords": ["milk", "safety", "consumption"], "response": "Milk from cows with mastitis should not be consumed or sold, as it may contain bacteria and antibiotics."},
        {"keywords": ["treatment", "cure", "heal"], "response": "Treatment includes consulting a veterinarian, administering antibiotics, and using proper milking techniques to relieve udder pressure."},
        {"keywords": ["antibiotics", "medication", "drug", "medicine"], "response": "Antibiotics like penicillin and amoxicillin are commonly used to treat bacterial infections causing mastitis."},
        {"keywords": ["natural", "remedies", "alternative", "home", "treatment"], "response": "Natural treatments include applying warm compresses to the udder, ensuring complete milking, and improving cow nutrition."},
        {"keywords": ["follow-up", "care", "recovery", "post-treatment"], "response": "Follow-up care involves monitoring milk quality, maintaining hygiene, and ensuring proper cow nutrition after treatment."},
        {"keywords": ["complications", "risks", "untreated", "problems"], "response": "Untreated mastitis can cause udder damage, reduced milk yield, systemic infections, and even death in severe cases."},
        {"keywords": ["udder", "swelling", "redness", "pain", "heat"], "response": "Mastitis often causes swelling, redness, heat, and pain in the cow's udder, making it uncomfortable for milking."},
        {"keywords": ["udder", "cleaning", "teat", "disinfect", "sanitation"], "response": "Clean udders and teat disinfection with pre- and post-milking dips are critical to preventing mastitis."},
        {"keywords": ["nutrition", "diet", "health", "vitamins"], "response": "Ensuring proper cow nutrition with a balanced diet rich in vitamins and minerals can strengthen immunity against mastitis."},
        {"keywords": ["stress", "management", "environment", "comfort"], "response": "Reducing environmental stress, overcrowding, and providing clean, comfortable bedding can help minimize mastitis risk."},
        {"keywords": ["chronic", "recurring", "persistent"], "response": "Chronic mastitis occurs when infections are not fully treated, leading to recurring inflammation and reduced milk production."},
        {"keywords": ["how", "treat", "steps"], "response": "To treat mastitis, consult a vet for antibiotics, apply warm compresses, ensure frequent milking, and keep the cow in a clean environment."},
        {"keywords": ["udder", "damage", "injury", "physical"], "response": "Physical injuries to the udder, such as cuts or bruises, increase susceptibility to mastitis and should be treated immediately."},
        {"keywords": ["bedding", "contamination", "cleanliness", "dirty"], "response": "Dirty bedding can harbor bacteria that cause mastitis, so it’s important to regularly clean and replace bedding materials."},
        {"keywords": ["identify", "detect", "early"], "response": "Early detection of mastitis involves observing milk consistency, udder swelling, and monitoring somatic cell counts."},
        {"keywords": ["economic", "loss", "impact"], "response": "Mastitis leads to significant economic losses due to reduced milk production, veterinary costs, and discarded milk."},
        {"keywords": ["vaccines", "immunity", "prevention"], "response": "Vaccines can help prevent certain types of mastitis by improving the cow's immunity against specific bacterial infections."},
        {"keywords": [ "days", "detect"], "response": "Mastitis can typically be detected within a few days of the onset of symptoms, but subclinical mastitis may require milk testing to identify, which can take longer."},
        {"keywords": ["long", "diagnosis"], "response": "Mastitis can usually be diagnosed within a few days of symptoms like swelling, redness, or changes in milk quality. However, subclinical mastitis may take longer to detect through milk tests."},
        {"keywords": ["detect", "time", "take"], "response": "The time it takes to detect mastitis depends on its type: clinical mastitis can be detected immediately due to visible symptoms, while subclinical mastitis may require several days for milk tests to show changes."},
        {"keywords": [ "fast", "diagnosed"], "response": "Mastitis is diagnosed relatively quickly, often within a few days, through a combination of physical examination, milk changes, and somatic cell count testing."},
        {"keywords": ["early", "detection", "symptoms"], "response": "Early detection of mastitis is important and can be achieved within a few days if there are visible symptoms or changes in milk quality. Subclinical cases may take longer to detect."},
        {"keywords": ["clinical", "subclinical", "difference"], "response": "Clinical mastitis shows visible symptoms like udder swelling, pain, and milk changes, making it easier to detect quickly. Subclinical mastitis may take longer to identify, as it lacks visible signs."},
        {"keywords": ["early","signs","diagnose"], "response": "Early signs of mastitis, such as slight swelling or changes in milk consistency, can usually be diagnosed within a few days, but more advanced tests may be needed for subclinical cases."},
        {"keywords": ["cost", "treat", "expense"], "response": "The cost of treating mastitis can vary depending on the severity of the condition, the type of treatment, and the veterinary care required. It may include expenses for veterinary consultation, antibiotics, diagnostics, and follow-up care. On average, treatment can range from $50 to $200 per cow, but severe cases or recurring mastitis may result in higher costs."},
        {"keywords": [ "detect", "early", "subclinical"], "response": "Early detection of subclinical mastitis often requires milk testing for somatic cell counts, which can take several days. Visible symptoms of clinical mastitis can be detected immediately."},
        {"keywords": ["detect", "early", "how", "long"], "response": "Early detection of mastitis can occur within a few days of symptom onset for clinical cases, while subclinical mastitis detection may take longer due to the need for milk testing."},
        {"keywords": ["detect", "early", "signs"], "response": "Early signs of mastitis include slight swelling, heat, and changes in milk consistency, which can be detected within a few days. Subclinical mastitis may take longer to diagnose with milk tests."},
        {"keywords": ["detect", "early", "milk", "changes"], "response": "Early detection of mastitis involves observing milk changes such as clots or abnormal consistency, along with udder swelling and heat, usually within a few days."},
        {"keywords": ["detect",  "early", "swelling", "pain"], "response": "Early signs of mastitis, like udder swelling and pain, can be detected quickly, while subclinical cases require milk testing, which may take several days."},
        {"keywords": ["detect", "early", "symptoms", "signs"], "response": "Early detection of mastitis includes recognizing symptoms like udder swelling, heat, and changes in milk consistency within a few days. Subclinical mastitis requires milk tests for confirmation."},
        {"keywords": ["detect",  "early", "diagnosis"], "response": "Early detection of mastitis is crucial and can usually be achieved within a few days of symptom onset for clinical cases. Subclinical mastitis may require more time for diagnosis through milk tests."}       
        ]
        self.default_response = "I'm sorry, I don't understand your question. Can you please rephrase it?"

    def get_response(self, user_input):
        user_input = user_input.lower()
        for entry in self.responses:
            for keyword in entry["keywords"]:
                if keyword in user_input:
                    return entry["response"]
        return self.default_response

chatbot = Chatbot()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chatbot.get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
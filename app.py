
from flask import Flask, request, render_template
from flask import jsonify
import pandas as pd
import pickle
import numpy as np
import time

model = pickle.load(open('hotel22.pkl', 'rb'))

# Mappings for displaying labels
hotel_mapping = { 0: "City Hotel", 1: "Resort Hotel" }
lead_time_mapping = {i: f"Day {i}" for i in range(1, 101)}
arrival_month_mapping = { 0: "April", 1: "August", 2: "December", 3: "February", 4: "January", 5: "July", 6: "June", 7: "March", 8: "May", 9: "November", 10: "October", 11: "September" }
stays_in_weekend_nights_mapping = {
  0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
  11: "11", 12: "12", 13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18", 19: "19"
}
stays_in_week_nights_mapping = {
  0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
  11: "11", 12: "12", 13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18", 19: "19", 
  20: "20", 21: "21", 22: "22", 23: "23", 24: "24", 25: "25", 26: "26", 27: "27", 28: "28", 
  29: "29", 30: "30", 31: "31", 32: "32", 33: "33", 34: "34", 35: "35", 36: "36", 37: "37", 
  38: "38", 39: "39", 40: "40", 41: "41", 42: "42", 43: "43", 44: "44", 45: "45", 46: "46", 
  47: "47", 48: "48", 49: "49", 50: "50"
}
adults_mapping = {
  0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
  11: "11", 12: "12", 13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18", 19: "19", 
  20: "20", 21: "21", 22: "22", 23: "23", 24: "24", 25: "25", 26: "26", 27: "27", 28: "28", 
  29: "29", 30: "30", 31: "31", 32: "32", 33: "33", 34: "34", 35: "35", 36: "36", 37: "37", 
  38: "38", 39: "39", 40: "40", 41: "41", 42: "42", 43: "43", 44: "44", 45: "45", 46: "46", 
  47: "47", 48: "48", 49: "49", 50: "50", 51: "51", 52: "52", 53: "53", 54: "54", 55: "55"
}
children_mapping = {
  0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10"
}
babies_mapping = {
  0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10"
}
meal_mapping = { 0: "BB", 1: "FB", 2: "HB", 3: "SC", 4: "Undefined" }
market_segment_mapping = { 0: "Aviation", 1: "Complementary", 2: "Corporate", 3: "Direct", 4: "Groups", 5: "Offline TA/TO", 6: "Online TA" }
is_repeated_guest_mapping = {0: "No", 1: "Yes"}
previous_cancellations_mapping = {
  0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
  11: "11", 12: "12", 13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18", 19: "19", 
  20: "20", 21: "21", 22: "22", 23: "23", 24: "24", 25: "25", 26: "26", 27: "27", 28: "28", 
  29: "29", 30: "30"
}
previous_bookings_not_canceled_mapping = {
  0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
  11: "11", 12: "12", 13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18", 19: "19", 
  20: "20", 21: "21", 22: "22", 23: "23", 24: "24", 25: "25", 26: "26", 27: "27", 28: "28", 
  29: "29", 30: "30", 31: "31", 32: "32", 33: "33", 34: "34", 35: "35", 36: "36", 37: "37", 
  38: "38", 39: "39", 40: "40", 41: "41", 42: "42", 43: "43", 44: "44", 45: "45", 46: "46", 
  47: "47", 48: "48", 49: "49", 50: "50", 51: "51", 52: "52", 53: "53", 54: "54", 55: "55", 
  56: "56", 57: "57", 58: "58", 59: "59", 60: "60", 61: "61", 62: "62", 63: "63", 64: "64", 
  65: "65", 66: "66", 67: "67", 68: "68", 69: "69", 70: "70", 71: "71", 72: "72"
}
reserved_room_type_mapping = { 0: "Accessible Room", 1: "Bungalow", 2: "Connecting Rooms", 3: "Deluxe", 4: "Apartment Style", 5: "Family", 6: "Standard", 7: "Adaptable", 8: "Loft", 9: "Penthouse" }
assigned_room_type_mapping = { 0: "Accessible Room", 1: "Bungalow", 2: "Connecting Rooms", 3: "Deluxe", 4: "Apartment Style", 5: "Family", 6: "Standard", 7: "Adaptable", 8: "Interconnecting", 9: "King Size", 10: "Loft", 11: "Penthouse" }
booking_changes_mapping = {
  0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10",
  11: "11", 12: "12", 13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18", 19: "19", 
  20: "20", 21: "21"
}
deposit_type_mapping = { 0: "No Deposit", 1: "Non Refund", 2: "Refundable" }
days_in_waiting_list_mapping = {i: f"Day {i}" for i in range(1, 371)}
customer_type_mapping = { 0: "Contract", 1: "Group", 2: "Transient", 3: "Transient-Party" }
adr_mapping = {i: f"Day {i}" for i in range(1, 1001)}
total_of_special_requests_mapping = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}
country_mapping = {
    0: "Aruba", 1: "Angola", 2: "Anguilla", 3: "Albania", 4: "Andorra", 5: "United Arab Emirates", 
    6: "Argentina", 7: "Armenia", 8: "American Samoa", 9: "Antarctica", 10: "French Southern Territories", 
    11: "Australia", 12: "Austria", 13: "Azerbaijan", 14: "Burundi", 15: "Belgium", 16: "Benin", 
    17: "Burkina Faso", 18: "Bangladesh", 19: "Bulgaria", 20: "Bahrain", 21: "Bahamas", 22: "Bosnia and Herzegovina", 
    23: "Belarus", 24: "Bolivia", 25: "Brazil", 26: "Barbados", 27: "Botswana", 28: "Central African Republic", 
    29: "Switzerland", 30: "Chile", 31: "China", 32: "Côte d'Ivoire", 33: "Cameroon", 34: "Congo", 
    35: "Colombia", 36: "Comoros", 37: "Cabo Verde", 38: "Costa Rica", 39: "Cuba", 40: "Cayman Islands", 
    41: "Cyprus", 42: "Czech Republic", 43: "Germany", 44: "Djibouti", 45: "Dominica", 46: "Denmark", 
    47: "Dominican Republic", 48: "Algeria", 49: "Ecuador", 50: "Egypt", 51: "Spain", 52: "Estonia", 
    53: "Ethiopia", 54: "Finland", 55: "Fiji", 56: "France", 57: "Faroe Islands", 58: "Gabon", 
    59: "United Kingdom", 60: "Georgia", 61: "Guernsey", 62: "Ghana", 63: "Gibraltar", 64: "Guadeloupe", 
    65: "Guinea-Bissau", 66: "Greece", 67: "Guatemala", 68: "Guyana", 69: "Hong Kong", 70: "Honduras", 
    71: "Croatia", 72: "Hungary", 73: "Indonesia", 74: "Isle of Man", 75: "India", 76: "Ireland", 
    77: "Iran", 78: "Iraq", 79: "Iceland", 80: "Israel", 81: "Italy", 82: "Jamaica", 83: "Jersey", 
    84: "Jordan", 85: "Japan", 86: "Kazakhstan", 87: "Kenya", 88: "Cambodia", 89: "Kiribati", 
    90: "Saint Kitts and Nevis", 91: "South Korea", 92: "Kuwait", 93: "Laos", 94: "Lebanon", 
    95: "Libya", 96: "Saint Lucia", 97: "Liechtenstein", 98: "Sri Lanka", 99: "Lithuania", 
    100: "Luxembourg", 101: "Latvia", 102: "Macao", 103: "Morocco", 104: "Monaco", 105: "Madagascar", 
    106: "Maldives", 107: "Mexico", 108: "North Macedonia", 109: "Mali", 110: "Malta", 111: "Myanmar", 
    112: "Montenegro", 113: "Mozambique", 114: "Mauritania", 115: "Mauritius", 116: "Malawi", 
    117: "Malaysia", 118: "Mayotte", 119: "Namibia", 120: "New Caledonia", 121: "Nigeria", 
    122: "Nicaragua", 123: "Netherlands", 124: "Norway", 125: "Nepal", 126: "New Zealand", 
    127: "Oman", 128: "Pakistan", 129: "Panama", 130: "Peru", 131: "Philippines", 132: "Palau", 
    133: "Poland", 134: "Puerto Rico", 135: "Portugal", 136: "Paraguay", 137: "French Polynesia", 
    138: "Qatar", 139: "Romania", 140: "Russia", 141: "Rwanda", 142: "Saudi Arabia", 
    143: "Sudan", 144: "Senegal", 145: "Singapore", 146: "Sierra Leone", 147: "El Salvador", 
    148: "San Marino", 149: "Serbia", 150: "São Tomé and Príncipe", 151: "Suriname", 
    152: "Slovakia", 153: "Slovenia", 154: "Sweden", 155: "Seychelles", 156: "Syria", 
    157: "Togo", 158: "Thailand", 159: "Tajikistan", 160: "East Timor", 161: "Tunisia", 
    162: "Turkey", 163: "Taiwan", 164: "Tanzania", 165: "Uganda", 166: "Ukraine", 
    167: "United States Minor Outlying Islands", 168: "Uruguay", 169: "United States", 
    170: "Uzbekistan", 171: "Venezuela", 172: "British Virgin Islands", 173: "Vietnam", 
    174: "South Africa", 175: "Zambia", 176: "Zimbabwe"
}

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return (render_template('index.html',
                               hotel_mapping=hotel_mapping,
                               lead_time_mapping=lead_time_mapping,  
                               arrival_month_mapping=arrival_month_mapping,
                               stays_in_weekend_nights_mapping=stays_in_weekend_nights_mapping,
                               stays_in_week_nights_mapping=stays_in_week_nights_mapping,
                               adults_mapping=adults_mapping,
                               children_mapping=children_mapping,
                               babies_mapping=babies_mapping,
                               meal_mapping=meal_mapping,
                               market_segment_mapping=market_segment_mapping,
                               is_repeated_guest_mapping=is_repeated_guest_mapping,
                               previous_cancellations_mapping=previous_cancellations_mapping,
                               previous_bookings_not_canceled_mapping=previous_bookings_not_canceled_mapping,
                               reserved_room_type_mapping=reserved_room_type_mapping,
                               assigned_room_type_mapping=assigned_room_type_mapping,
                               booking_changes_mapping=booking_changes_mapping,
                               deposit_type_mapping=deposit_type_mapping,
                               days_in_waiting_list_mapping=days_in_waiting_list_mapping,  
                               customer_type_mapping=customer_type_mapping,
                               adr_mapping=adr_mapping, 
                               total_of_special_requests_mapping=total_of_special_requests_mapping,
                               country_mapping=country_mapping))


# @app.route('/estimate', methods=['POST'])
# def predict():
#     try:
#         int_features = [int(x) for x in request.form.values()]
#         features = [np.array(int_features)]
#         prediction = model.predict(features)[0]
#         return jsonify({'prediction_text': 'Risk of Cancellation is {}'})
#     except ValueError:
#         error_message = 'Oops! Looks like you left something out...Please complete your selection.'
#         return jsonify({'error': error_message})


# if __name__ == '__main__':
#     app.run(debug=True)




    
    
@app.route('/estimate', methods=['POST'])
def predict():
  if request.method == 'POST':
        form_data = request.form
        print("Received Form Data:", form_data)  # Debugging: Print out form data
  try:
        # Retrieve the form values
        form_values = request.form.values()

        # Convert form values to integers
        int_features = []
        for x in form_values:
            if x.strip():  # Check if the field is not empty
                int_features.append(int(x))
            else:
                raise ValueError("Missing input")

        # Create features array
        features = [np.array(int_features)]
        
        # Make prediction using the classification model (0 or 1)
        prediction = model.predict(features)[0]
        
        # Map the prediction to 'Not Likely' or 'Very Likely'
        prediction_text = 'Very Likely' if prediction == 1 else 'Not Likely'
        
        return jsonify({'prediction_text': f'Risk of Cancellation is {prediction_text}', 'prediction': int(prediction)})
    
  except Exception as e:
        # Catch any other unexpected errors
        return jsonify({'error': 'An unexpected error occurred. Please try again.'})

if __name__ == '__main__':
    app.run(debug=True)

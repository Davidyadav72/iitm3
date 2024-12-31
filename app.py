from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('david.html')

@app.route('/make_payment', methods=['POST'])
def make_payment():
    # Extract UPI ID (This can be processed if needed)
    upi_id = request.form.get('upi_id')
    
    if not upi_id:
        return "UPI ID is required", 400

    # In a real-world scenario, you would integrate with the payment gateway for verification
    # For now, we'll just simulate redirection to PhonePe
    upi_link = f"upi://pay?pa=9369179899@ibl&pn=David%20Yadav&am=30&cu=INR&tid=1234567890&url=https://www.yourpaymenturl.com"
    
    # Redirect to the UPI app (PhonePe or any UPI app installed on the user's device)
    return redirect(upi_link)

if __name__ == '__main__':
    app.run(debug=True)

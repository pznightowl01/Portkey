// Razorpay Payment Integration for Portkey

function initiatePayment() {
    // Create order on backend
    fetch('/create-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error creating order: ' + data.error);
            return;
        }
        
        // Open Razorpay checkout
        openRazorpayCheckout(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Payment initiation failed. Please try again.');
    });
}

function openRazorpayCheckout(orderData) {
    const options = {
        key: orderData.key_id,
        amount: orderData.amount,
        currency: orderData.currency,
        name: 'Portkey Food Ordering',
        description: 'Food Order Payment',
        order_id: orderData.order_id,
        handler: function(response) {
            // Payment successful, verify on backend
            verifyPayment(response);
        },
        prefill: {
            name: '',
            email: '',
            contact: ''
        },
        theme: {
            color: '#ea580c'
        },
        modal: {
            ondismiss: function() {
                alert('Payment cancelled. Your cart is still saved.');
            }
        }
    };
    
    const razorpay = new Razorpay(options);
    razorpay.open();
}

function verifyPayment(response) {
    // Submit payment details to backend for verification
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/verify-payment';
    
    const fields = [
        { name: 'razorpay_payment_id', value: response.razorpay_payment_id },
        { name: 'razorpay_order_id', value: response.razorpay_order_id },
        { name: 'razorpay_signature', value: response.razorpay_signature }
    ];
    
    fields.forEach(field => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = field.name;
        input.value = field.value;
        form.appendChild(input);
    });
    
    document.body.appendChild(form);
    form.submit();
}

// Add event listener to checkout button
document.addEventListener('DOMContentLoaded', function() {
    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            initiatePayment();
        });
    }
});

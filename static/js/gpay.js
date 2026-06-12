/**
 * Google Pay integration for Portkey food delivery app
 * Based on Google Pay Web SDK documentation
 */

const baseRequest = {
  apiVersion: 2,
  apiVersionMinor: 0
};

const allowedCardNetworks = ["AMEX", "DISCOVER", "INTERAC", "JCB", "MASTERCARD", "VISA"];
const allowedCardAuthMethods = ["PAN_ONLY", "CRYPTOGRAM_3DS"];

const tokenizationSpecification = {
  type: 'PAYMENT_GATEWAY',
  parameters: {
    'gateway': 'example',
    'gatewayMerchantId': 'exampleGatewayMerchantId'
  }
};

const baseCardPaymentMethod = {
  type: 'CARD',
  parameters: {
    allowedAuthMethods: allowedCardAuthMethods,
    allowedCardNetworks: allowedCardNetworks
  }
};

const upiPaymentMethod = {
  type: 'UPI',
  parameters: {
    payeeVpa: 'merchant@psp',
    payeeName: 'Portkey Food Delivery'
  }
};

const googlePayClient = null;

function getGooglePaymentsClient() {
  if (googlePayClient === null) {
    googlePayClient = new google.payments.api.PaymentsClient({environment: 'TEST'});
  }
  return googlePayClient;
}

function getGoogleIsReadyToPayRequest() {
  return Object.assign(
    {},
    baseRequest,
    {
      allowedPaymentMethods: [baseCardPaymentMethod, upiPaymentMethod]
    }
  );
}

function getGooglePaymentDataRequest() {
  const paymentDataRequest = Object.assign({}, baseRequest);
  paymentDataRequest.allowedPaymentMethods = [baseCardPaymentMethod, upiPaymentMethod];
  paymentDataRequest.transactionInfo = getGoogleTransactionInfo();
  paymentDataRequest.merchantInfo = {
    merchantName: 'Portkey Food Delivery',
    merchantId: '01234567890123456789'
  };
  paymentDataRequest.callbackIntents = ["PAYMENT_AUTHORIZATION"];
  paymentDataRequest.paymentDataCallbacks = {
    onPaymentAuthorized: onPaymentAuthorized
  };
  return paymentDataRequest;
}

function getGoogleTransactionInfo() {
  return {
    displayItems: [
      {
        label: "Subtotal",
        type: "SUBTOTAL",
        price: window.cartData ? window.cartData.subtotal : "0.00",
      },
      {
        label: "Tax",
        type: "TAX",
        price: window.cartData ? window.cartData.tax : "0.00",
      }
    ],
    countryCode: 'IN',
    currencyCode: "INR",
    totalPriceStatus: "FINAL",
    totalPrice: window.cartData ? window.cartData.total : "0.00",
    totalPriceLabel: "Total"
  };
}

function onPaymentAuthorized(paymentData) {
  return new Promise(function(resolve, reject) {
    // Handle the response
    processPayment(paymentData)
      .then(function() {
        resolve({transactionState: 'SUCCESS'});
      })
      .catch(function() {
        resolve({
          transactionState: 'ERROR',
          error: {
            intent: 'PAYMENT_AUTHORIZATION',
            message: 'Insufficient funds',
            reason: 'PAYMENT_DATA_INVALID'
          }
        });
      });
  });
}

function onGooglePayLoaded() {
  const googlePayClient = getGooglePaymentsClient();
  googlePayClient.isReadyToPay(getGoogleIsReadyToPayRequest())
    .then(function(response) {
      if (response.result) {
        addGooglePayButton();
      }
    })
    .catch(function(err) {
      console.error("Google Pay error:", err);
    });
}

function addGooglePayButton() {
  const paymentsClient = getGooglePaymentsClient();
  const button = paymentsClient.createButton({
    onClick: onGooglePaymentButtonClicked,
    allowedPaymentMethods: [baseCardPaymentMethod, upiPaymentMethod]
  });
  document.getElementById('gpay-button-container').appendChild(button);
}

function onGooglePaymentButtonClicked() {
  const paymentDataRequest = getGooglePaymentDataRequest();
  paymentDataRequest.transactionInfo = getGoogleTransactionInfo();

  const paymentsClient = getGooglePaymentsClient();
  paymentsClient.loadPaymentData(paymentDataRequest)
    .then(function(paymentResponse) {
      processPayment(paymentResponse);
    })
    .catch(function(err) {
      console.error('Google Pay payment failed:', err);
    });
}

function processPayment(paymentResponse) {
  return new Promise(function(resolve, reject) {
    // Extract payment token
    const paymentToken = paymentResponse.paymentMethodData.tokenizationData.token;

    // Send to server for processing
    fetch('/process-gpay-payment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        paymentToken: paymentToken,
        cartData: window.cartData
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Redirect to success page
        window.location.href = '/thank-you';
      } else {
        alert('Payment failed: ' + data.error);
        reject(new Error(data.error));
      }
    })
    .catch(error => {
      console.error('Payment processing error:', error);
      alert('Payment processing failed. Please try again.');
      reject(error);
    });
  });
}

// Initialize Google Pay when page loads
document.addEventListener('DOMContentLoaded', function() {
  if (document.getElementById('gpay-button-container')) {
    onGooglePayLoaded();
  }
});

importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyAX6Y0jlwOK-l_5blmUyTwA21SXGObTS0E",
  authDomain: "sales-dashboard-c3227.firebaseapp.com",
  projectId: "sales-dashboard-c3227",
  storageBucket: "sales-dashboard-c3227.firebasestorage.app",
  messagingSenderId: "15514100041",
  appId: "1:15514100041:web:26ecc6379d505eff123a98"
});

const messaging = firebase.messaging();

// バックグラウンド通知の受信
messaging.onBackgroundMessage(function(payload) {
  const { title, body } = payload.notification;
  self.registration.showNotification(title, {
    body: body,
    icon: '/sales-dashboard/icon-192.png'
  });
});

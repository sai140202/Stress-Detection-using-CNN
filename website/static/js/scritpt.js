
function AddDetails(name,gender,email,role , number)
{

 const name1 = document.getElementById("name");
 const gender1 = document.getElementById("gender");
 const email1 = document.getElementById("email");
 const role1 = document.getElementById("roles");
 const number1 = document.getElementById("number");
 const avatarElement = document.getElementById('avatar');


 let avatarSrc;
if (gender === 'male') {
  avatarSrc = '../static/css/male.jpg';
} else {
  avatarSrc = '../static/css/female.png';
}

avatarElement.src = avatarSrc ;
 name1.innerHTML = name;
 gender1.innerHTML = gender;
 email1.innerHTML = email;
 role1.innerHTML = role;
 number1.innerHTML = number;


}
   

       import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
       import { getDatabase,set ,ref , child, get ,onValue} from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";
       import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-analytics.js";
       import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut,onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-auth.js";
       // TODO: Add SDKs for Firebase products that you want to use
       // https://firebase.google.com/docs/web/setup#available-libraries
 
       // Your web app's Firebase configuration
       // For Firebase JS SDK v7.20.0 and later, measurementId is optional
       const firebaseConfig = {
       apiKey: "AIzaSyCr_-XEuiGMItFQ_NjXeCY5Q9cuUqUp9lo",
       authDomain: "stress-detection-fffaa.firebaseapp.com",
       projectId: "stress-detection-fffaa",
       storageBucket: "stress-detection-fffaa.appspot.com",
       messagingSenderId: "835851634384",
       appId: "1:835851634384:web:a7c64cfc67defea8db00d5",
       measurementId: "G-8NB1JD9QK0"
     };
 
       // Initialize Firebase
       const app = initializeApp(firebaseConfig);
       const analytics = getAnalytics(app);
     const database = getDatabase(app);
     const auth = getAuth(app);
 
 
     onAuthStateChanged(auth, (user) => {
     if (user) {
       // User is signed in, see docs for a list of available properties
       // https://firebase.google.com/docs/reference/js/firebase.User
       const uid = user.uid;
       const user1 = auth.currentUser;
       // console.log(uid);
       // console.log(user1);

       const userDetailsRef = ref(database, `users/${user.uid}`);
onValue(userDetailsRef, (snapshot) => {
const data = snapshot.val();
// Do something with the userDetails object
     let name = data.name;
         let gender = data.gender;
         let email = data.email;
         let role = data.roles;
         let number = data.number;
         AddDetails(name, gender , email ,role , number);

});
} else {
       // User is signed out
       // ...
     }
   });


   
 
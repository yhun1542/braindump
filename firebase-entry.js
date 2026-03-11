// Firebase SDK 번들 entry - galaxy.html에서 사용하는 모든 함수 export
export { initializeApp, getApps, getApp } from 'firebase/app';
export {
  getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged,
  browserLocalPersistence, browserSessionPersistence, setPersistence,
  sendPasswordResetEmail
} from 'firebase/auth';
export {
  getFirestore, collection, doc, setDoc, getDoc, getDocs,
  deleteDoc, updateDoc, onSnapshot, query, orderBy, serverTimestamp, addDoc
} from 'firebase/firestore';
export {
  getStorage, ref as storageRef, uploadBytes, getDownloadURL
} from 'firebase/storage';

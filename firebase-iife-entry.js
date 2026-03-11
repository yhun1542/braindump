// Firebase SDK를 window.FirebaseSDK로 노출 (IIFE 번들용)
import { initializeApp, getApps, getApp } from 'firebase/app';
import {
  getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged,
  browserLocalPersistence, browserSessionPersistence, setPersistence,
  sendPasswordResetEmail
} from 'firebase/auth';
import {
  getFirestore, collection, doc, setDoc, getDoc, getDocs,
  deleteDoc, updateDoc, onSnapshot, query, orderBy, serverTimestamp, addDoc
} from 'firebase/firestore';
import { getStorage, ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage';

window.FirebaseSDK = {
  initializeApp, getApps, getApp,
  getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged,
  browserLocalPersistence, browserSessionPersistence, setPersistence,
  sendPasswordResetEmail,
  getFirestore, collection, doc, setDoc, getDoc, getDocs,
  deleteDoc, updateDoc, onSnapshot, query, orderBy, serverTimestamp, addDoc,
  getStorage, storageRef, uploadBytes, getDownloadURL
};

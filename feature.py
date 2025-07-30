from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import tensorflow as tf
text = { 'I like pizza', 'I like pasta', 'I dislike burgers'}
import cv2 as cv 
tf.fit(text)
print(cv.get_feature_names_out())
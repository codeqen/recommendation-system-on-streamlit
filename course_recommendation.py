import streamlit as st
from pymongo import MongoClient
import altair as alt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

@st.cache(hash_funcs={MongoClient: id})
def mongo_connect(url):
    return MongoClient(url)

client = mongo_connect("mongodb+srv://simran:simran@cluster0.gd0d5.azure.mongodb.net/simran?retryWrites=true&w=majority")
db = client.students

st.title("TEST YOUR PYTHON SKILLS !!!")
st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)

#demographics of the student--------------------->
student_name = st.text_input('Full Name')
country = st.text_input('Country')
age = st.number_input('Age',min_value = 1,format = '%d')

st.markdown('**Pick any one option for the given question!**')

answer_key = ['Hello foo and bin','None of the above','List is mutable and Tuple is immutable', 'Bye World','Every class must have a constructor','An object','FIFO','Depth','h = O(log n)','4','16','Error','O(NlogN)','Bellmen Ford Shortest path algorithm', 'Tower of hanoi']
student_answer = [None] *15


#Questions-------------------------->
Q1 = st.write("Q1 :  What will be the output of the following Python code?")
code1 = '''print("Hello {name1} and {name2}".format(name1='foo', name2='bin'))'''
st.code(code1, language = 'python')
A1 = st.radio('',('Hello foo and bin','Hello {name1} and {name2}','Hello and','Error'))
student_answer[0] = A1

A2 = st.radio('Q2 :  What is the maximum possible length of an identifier?',('32 characters','64 characters','79 characters','None of the above'))
student_answer[1] = A2

A3 = st.radio('Q3 :  Which statement is correct ?',('List is mutable and Tuple is immutable','List is immutable and Tuple is mutable','Both are Immutable','Both are mutable'))
student_answer[2] = A3

Q4 = st.write("Q4 :  What will be the output of the following Python code?")
code2 = ''' class test:
def __init__(self):
    print "Hello World"
def __init__(self):
    print "Bye World"
obj=test()'''
st.code(code2, language='python')
A4 = st.radio('',('Hello World','Compilation Error','Bye World','Ambiguity'))
student_answer[3] = A4

Q5 = st.write("Q5 :  Which of the following is False with respect Python code?")
code2 = '''class Student:

	def __init__(self,id,age):

		self.id=id

		self.age=age 
 std=Student(1,20)
       '''
st.code(code2, language='python')
A5 = st.radio('',('"std" is the reference variable for object Student(1,20)','id and age are called the parameters','Every class must have a constructor','None of the above'))
student_answer[4] = A5

A6 = st.radio('Q6 :  _____ represents an entity in the real world with its identity and behaviour. ', ('A method','A class','An object', 'An operator'))
student_answer[5] = A6

A7 = st.radio('Q7 :  Queue data structure works on',('LIFO','FIFO','FILO','none of the above'))
student_answer[6]= A7

A8 = st.radio('Q8 :  The number of edges from the root to the node is called __________ of the tree.',('Height','Depth','Length','Width'))
student_answer[7] = A8

A9 = st.radio('Q9 :  What is the average case time complexity for finding the height of the binary tree?',('h = O(loglogn)','h = O(nlogn)',' h = O(n)','h = O(log n)'))
student_answer[8] = A9

A10 = st.radio('Q10 :  What would "print(9//2)" return?',('4.5','4.0','4','Error'))
student_answer[9] = A10

A11 = st.radio('Q11 :  What would "print(4**2)" return?',('16','8','4','Error'))
student_answer[10] = A11

Q12 = st.write("Q12 :  What will be the output of the following Python code?")
code12 = '''i = 0
while i < 3:
       print i
       i++
       print i+1'''
st.code(code12, language = 'python')
A12 = st.radio('',('0 2 1 3 2 4','0 1 2 3 4 5','1 0 2 4 3 5','Error'))
student_answer[11] = A12

A13 = st.radio("Q13 :  What is the time complexity of Huffman Coding?",('O(logN)','O(NlogN)','O(n)','O(n^2)'))
student_answer[12] = A13

A14 = st.radio("Q14 :  Which of the following standard algorithms is not a Greedy algorithm?",('Dijkstra shortest path algorithm','Prims algorithm','Bellmen Ford Shortest path algorithm','Kruskal algorithm'))
student_answer[13] = A14

A15 = st.radio("Q15 :  Which of the following is not a backtracking algorithm?",('N queen problem','M colouring problem','Tower of hanoi','Knight tour problem'))
student_answer[14] = A15



#calculate marks------------------>

marks = [0]*15
if st.button('GET RESULTS'):
    for i in range(15):
        if answer_key[i] == student_answer[i]:
            marks[i] = 1
        else:
            marks[i] = 0  
    logic = ((marks[9]+marks[10]+marks[11])/3)*100
    syntax = ((marks[0]+marks[1]+marks[2])/3)*100
    oops_concept = ((marks[3]+marks[4]+marks[5])/3)*100
    data_structures = ((marks[6]+marks[7]+marks[8])/3)*100
    algorithms = ((marks[12]+marks[13]+marks[14])/3)*100

    data = pd.DataFrame({'sub_topics':['logic','syntax','oops_concept','data_structures','algorithms'],'performance': [logic,syntax,oops_concept,data_structures,algorithms]})
    st.write(data)
    st.altair_chart(alt.Chart(data).mark_bar().encode(x=alt.X('sub_topics', sort=None),y='performance').interactive())

    #Saving to Database--------------------------------->
    mongo_dump = { "Name" : student_name,
             "Country" : country,
             "Age": age,
             "logic_Marks": logic,
             "syntax_Marks": syntax,
             "oops_Marks": oops_concept,
             "Data_structures_Marks": data_structures,
             "algorithm_Marks": algorithms
             }
    try:
        mongo_dump_result = db.data.insert_one(mongo_dump)
        st.write('Your data is safe with us!')
    
    except:
        st.error("Sorry, looks like we ran into an error! :cry:")         

    #Machine Learning Algorithm----------------------------->
    for_prediction = [(marks[9]+marks[10]+marks[11]),(marks[0]+marks[1]+marks[2]),(marks[3]+marks[4]+marks[5]),(marks[6]+marks[7]+marks[8]),(marks[12]+marks[13]+marks[14])]
    data = pd.read_csv('/home/ganesh/Desktop/app/df.csv')
    X = data.iloc[:,0:5]
    model = KMeans(n_clusters = 3, random_state = 0)
    labels = model.fit(X)
    prediction = model.predict([for_prediction])
    st.title("HERE ARE SOME RECOMMENDATIONS FOR YOU!")
    if prediction == [0] :
        st.write('Beginner Course')
    elif prediction == [1]:
        st.write('Intermediate Course')
    elif prediction == [2]:
        st.write('Advanced Course')

import pickle
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
import mplcursors

# Load the saved model from file
with open('MLP_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

with open('scaler_object.pkl', 'rb') as g:
    scaler_object = pickle.load(g)

    
#Load the saved dataset from a csv file
df = pd.read_csv('Bank_dataset.csv')
df['churn']=['No churn' if val == 0 else 'Churn' for val in df['churn']]

data = df.copy()


def main():
    
    st.set_page_config(
        page_title="Churn prediction",
        layout='wide'
    )
    st.write(
        '<h1 style="text-align: center; padding-top: 20px;color: #115f9a">Customer Churn For ABC Bank</h1>',
        unsafe_allow_html=True)
    st.sidebar.title("Churn prediction")
    credit_score = st.sidebar.number_input("Credit Score")
    country = st.sidebar.selectbox("Country",('France','Germany','Spain'))
    age = st.sidebar.number_input('Age')
    balance=st.sidebar.number_input('Balance')
    products_number = st.sidebar.number_input('Products Number')
    active_member = st.sidebar.selectbox('Active Member',('Yes','No'))
 
    estimated_salary=st.sidebar.number_input('Salary')

    # When 'Predict' is clicked, make the prediction and display the result
    if st.sidebar.button("Predict"): 
        result = prediction(credit_score,country,age,balance,products_number,active_member,estimated_salary)
        st.sidebar.success('Customer has {}'.format(result))


        
    # Add content to the three columns
    col1, col_emp, col2, col_emp2, col3 = st.columns([400,100,400,80,400])

       
       
        # Add content to the first column
    with col1:
        # Bin the tenure column
        bins = [0, 2, 4, 6, 8, 10]
        labels = ['0-2', '2-4', '4-6', '6-8', '8-10']
        df['tenure_bin'] = pd.cut(df['tenure'], bins=bins, labels=labels)

        color_scheme = alt.Scale(domain=['Churn','No churn'], range=['brown','green'])
        horizontal_bar_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('count()', axis=alt.Axis(title='Count')),
    y=alt.Y('tenure_bin:N', axis=alt.Axis(labelAngle=0, labelAlign='left')),
    color=alt.Color('churn', scale=color_scheme, title="Churn"),
    row=alt.Row('gender:N', header=alt.Header(title='Gender', labelAlign='center')),
    tooltip=['gender', 'churn', alt.Text('count()', format=',')]
            ).properties(
                width=200,
                height=150,
                title={
                "text": "Customer Tenure and Gender",
                "align": "center",
                "anchor": "middle"}
            )
        
    col1.altair_chart(horizontal_bar_chart,use_container_width=False)


 # Visualization 2: Stacked bar chart
    stacked_data = data.groupby(["country", "gender", "active_member", "churn"])["customer_id"].count().unstack().fillna(0)
    stacked_data = stacked_data.reset_index().melt(id_vars=["country", "gender", "active_member"], var_name="churn", value_name="count")
    stacked_chart = alt.Chart(stacked_data).mark_bar().encode(
            x=alt.X("country", sort=alt.SortField("count", order="descending")),
            y=alt.Y("count"),
            color=alt.Color("churn", scale=alt.Scale(scheme="category10")),
            column=alt.Column("active_member"),
            row=alt.Row("gender")
        ).properties(
            width=100,
            height=100,
            title={
                "text": "Churn by Country and Gender",
                "align": "center",
                "anchor": "middle"
            }

        )
        

    col1.altair_chart(stacked_chart,use_container_width=False)


# Add content to the second column
    with col2:
            # Calculate the number of male and female customers

        # group values by 'gender' adf¸nd 'country'
        #grouped = df.groupby(['gender', 'country']).size()

        df['churn']=['No churn' if val == 0 else 'Churn' for val in df['churn']]
        churned = df[df['churn'] == 'Churn']
        bins = [0, 30, 40, 50, 60,100]
        labels = ['0-30 (yrs)', '30-40 (yrs)', '40-50 (yrs)', '50-60 (yrs)', '60-100 (yrs)']
        churned['age_bins'] = pd.cut(churned['age'], bins=bins, labels=labels)

        # Group the data by age bins
        grouped = churned.groupby('age_bins').size()


        # Calculate percentage of each group
        #total = grouped.sum()
        #percentages = [round((size/total)*100, 2) for size in grouped]

        # Create pie chart
        fig, ax = plt.subplots(figsize=(9,9))
        fig.suptitle('Age Distribution for churned Customers',fontsize=25)

        # Set the width of the wedges to create a doughnut chart
        # Set the width of the wedges to create a doughnut chart
        wedgeprops = {'width': 0.6, 'edgecolor': 'white'}
        wedges, labels, autopct = ax.pie(grouped, labels=labels, autopct='%1.1f%%', wedgeprops=wedgeprops,
                                 textprops={'fontsize': 22})

        # Set the cursor style
        import mplcursors
        cursor = mplcursors.cursor(ax, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f'{sel.label}\n{percentages[sel.index]}%'))

        # Customize appearance of pie chart
        ax.axis('equal')  # Make the chart circular
        plt.setp(labels, fontsize=25)
        st.pyplot(fig)

       
        
        st.metric(label="Returned", value=555)

        
        st.metric(label="Total churned", value=2037)

        Percentage= round((555/2037) * 100,0)
        st.metric(label="Returned Customers (%)", value=Percentage)
    


        # Add content to the third column
    with col3:
        color_scheme = alt.Scale(domain=['No churn','Churn'], range=['navy','blue'])
        stacked_bar_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('country:N', axis=alt.Axis(labelAngle=0, labelAlign='center')),
                y=alt.Y('count()', axis=alt.Axis(title='Count')),
                color=alt.Color('churn', scale=color_scheme,title="Churn"),
                column=alt.Column('gender:N', header=alt.Header(title='Gender', labelAlign='center')),
                tooltip=['gender', 'country', 'churn', alt.Text('count()', format=',')]
            ).properties(
                width=220,
                height=300,
                title={
                "text": "churn by country , balance and gender",
                "align": "center",
                "anchor": "middle"
            }

            )
        col3.altair_chart(stacked_bar_chart,use_container_width=False)


# Create a Customer Product Number-Gender Bar chart
        
        color_scheme = alt.Scale(domain=['Churn','No churn'], range=['red','green'])
        horizontal_bar_chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('count()', axis=alt.Axis(title='Count')),
    y=alt.Y('products_number:N', axis=alt.Axis(labelAngle=0, labelAlign='center')),
    color=alt.Color('churn', scale=color_scheme, title="Churn"),
  #  row=alt.Row('gender:N', header=alt.Header(title='Gender', labelAlign='center')),
    tooltip=['gender', 'churn', alt.Text('count()', format=',')]
            ).properties(
                width=400,
                height=300,
                title={
                "text": "Customer Tenure and Gender",
                "align": "center",
                "anchor": "middle"}
            )
        
        col3.altair_chart(horizontal_bar_chart,use_container_width=False)



# PREDICTIONS START HERE
# customer_id	credit_score	country	gender	age	tenure	balance	products_number	credit_card	active_member	estimated_salary churn


def prediction(credit_score,country,age,balance,products_number,active_member,estimated_salary):   
    
    TENURE =0
    # Pre-processing user input 
    credit_score == float(credit_score)
    if country == 'France':
        country = 1
    elif country == 'Germany':
        country = 2
    else:
        country = 3

    age = float(age)
    balance = float(balance)
    products_number = float(products_number)
    if active_member == 'Yes':
        active_member = 1
    else:
        active_member = 0
    estimated_salary = float(estimated_salary)

    # Scaling
    my_input = {'credit_score':credit_score,'country':country,'age':age,'tenure':TENURE,'balance':balance,'products_number':products_number,'active_member':active_member,'estimated_salary':estimated_salary}
    my_input_df = pd.DataFrame(my_input,index = [0])
    my_input_df[['credit_score','tenure','balance','products_number','estimated_salary']]= scaler_object.transform(my_input_df[['credit_score','tenure','balance','products_number','estimated_salary']])



 
    # Making predictions 
    prediction = loaded_model.predict(my_input_df[['credit_score','country','age','balance','products_number','active_member','estimated_salary']])
     
    if prediction == 0:
        pred = 'No Churn'
    else:
        pred = 'Churn'
    return pred



 

   

if __name__ == "__main__":
     main()
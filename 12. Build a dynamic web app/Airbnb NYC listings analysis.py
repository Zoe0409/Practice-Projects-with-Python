import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache
def get_data():
    url = "http://data.insideairbnb.com/united-states/ny/new-york-city/2019-09-12/visualisations/listings.csv"
    return pd.read_csv(url)

df = get_data()


st.title("Airbnb NYC listings data analysis")
st.markdown("Airbnb does not officially release any of its data. Another group called Inside Airbnb periodically releases Airbnb listings and review data.")
st.header("Airbnb NYC listings: data at a glance")
st.markdown("The first five records of the Airbnb data we downloaded.")
st.dataframe(df.head())

st.subheader("Selecting a subset of columns")
st.write(f"Out of the {df.shape[1]} columns, select what features you want to view.")
defaultcols = ["name", "host_name", "neighbourhood", "room_type", "price"]
cols = st.multiselect("Columns", df.columns.tolist(), default=defaultcols)
st.dataframe(df[cols].head(10))

st.header("Where are the most expensive properties located?")
st.subheader("On a map")

st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")
st.map(df.query("price>=800")[["latitude", "longitude"]].dropna(how="any"))

st.subheader("In a table")
st.markdown("Following are the top five most expensive properties.")
st.write(df.query("price>=800").sort_values("price", ascending=False).head())

st.header("Average price by room type")
st.table(df.groupby("room_type").price.mean().reset_index()\
    .round(2).sort_values("price", ascending=False)\
    .assign(avg_price=lambda x: x.pop("price").apply(lambda y: "%.2f" % y)))

st.header("Which host has the most properties listed?")
listingcounts = df.host_id.value_counts()
top_host_1 = df.query('host_id==@listingcounts.index[0]')
top_host_2 = df.query('host_id==@listingcounts.index[1]')
st.write(f"""**{top_host_1.iloc[0].host_name}** is at the top with {listingcounts.iloc[0]} property listings.
**{top_host_2.iloc[1].host_name}** is second with {listingcounts.iloc[1]} listings. Following are randomly chosen
listings from the two displayed as JSON using [`st.json`](https://streamlit.io/docs/api.html#streamlit.json).""")

st.json({top_host_1.iloc[0].host_name: top_host_1\
    [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
        .sample(2, random_state=4).to_dict(orient="records"),
        top_host_2.iloc[0].host_name: top_host_2\
    [["name", "neighbourhood", "room_type", "minimum_nights", "price"]]\
        .sample(2, random_state=4).to_dict(orient="records")})

st.header("What is the distribution of property price?")
st.write("""Select a customized price range from the side bar to update the histogram below displayed as a Plotly chart using
[`st.plotly_chart`](https://streamlit.io/docs/api.html#streamlit.plotly_chart).""")
min_values, max_values = st.sidebar.slider("Select a price range", int(df.price.min()), int(df.price.clip(upper=1000.).max()), [50, 300])
f = px.histogram(df[df.price.between(min_values, max_values)], x="price", nbins=15, title="Price distribution")
f.update_xaxes(title="Price")
f.update_yaxes(title="No. of listings")
st.plotly_chart(f)

st.header("What is the distribution of availability in various neighborhoods?")
st.write("Using a radio button restricts selection to only one option at a time.")
neighborhood = st.radio("Neighborhood", df.neighbourhood_group.unique())
show_exp = st.checkbox("Include expensive listings")
show_exp = " and price<200" if not show_exp else ""

@st.cache
def get_availability(show_exp, neighborhood):
    return df.query(f"""neighbourhood_group==@neighborhood{show_exp}\
        and availability_365>0""").availability_365.describe(\
            percentiles=[.1, .25, .5, .75, .9, .99]).to_frame().T

st.table(get_availability(show_exp, neighborhood))
st.write("At 169 days, Brooklyn has the lowest average availability. At 226, Staten Island has the highest average availability.\
    If we include expensive listings (price>=$200), the numbers are 171 and 230 respectively.")
st.markdown("_**Note:** There are 18431 records with `availability_365` 0 (zero), which I've ignored._")

df.query("availability_365>0").groupby("neighbourhood_group")\
    .availability_365.mean().plot.bar(rot=0).set(title="Average availability by neighborhood group",
        xlabel="Neighborhood group", ylabel="Avg. availability (in no. of days)")
st.pyplot()

st.header("Properties by number of reviews")
st.write("Enter a range of numbers in the sidebar to view properties whose review count falls in that range.")
minimum = st.sidebar.number_input("Minimum number of reviews:", min_value=0, max_value=int(df.number_of_reviews.max()), value = 5)
maximum = st.sidebar.number_input("Maximum number of reviews:", min_value=0, max_value=int(df.number_of_reviews.max()), value=50)
if minimum > maximum:
    st.error("Please enter a valid range")
else:
    df.query("@minimum<=number_of_reviews<=@maximum").sort_values("number_of_reviews", ascending=False)\
        .head(50)[["name", "number_of_reviews", "neighbourhood", "host_name", "room_type", "price"]]

st.write("486 is the highest number of reviews and two properties have it. Both are in the East Elmhurst \
    neighborhood and are private rooms with prices $65 and $45. \
    In general, listings with >400 reviews are priced below $100. \
    A few are between $100 and $200, and only one is priced above $200.")



st.header("Just For Fun")
st.write("> Cute and adorable images!!!")
pics = {
    "Cat": "https://cdn.pixabay.com/photo/2016/09/24/22/20/cat-1692702_960_720.jpg",
    "Puppy": "https://cdn.pixabay.com/photo/2019/03/15/19/19/puppy-4057786_960_720.jpg",
    "Sci-fi city": "https://storage.needpix.com/rsynced_images/science-fiction-2971848_1280.jpg"
}
pic = st.selectbox("Picture choices:", list(pics.keys()), 0)
st.image(pics[pic], use_column_width=True, caption=pics[pic])


btn = st.button("Try this button!")
if btn:
    st.balloons()



import streamlit as st
import pandas as pd
from cnsenti import Emotion, Sentiment
import jieba
import re
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from streamlit_echarts import st_pyecharts

st.title("cnsenti App")
st.markdown("""
*这是中文情感分析**[cnsenti库](https://github.com/thunderhit/cnsenti) **对应的测试网站，可以提供简单中文文本的情绪及情感计算。*
""")

st.title('准备数据')
uploaded_file = st.file_uploader(label='可以对自有的CSV文件进行上传、分析情感、制作词云图', type=['csv'])
st.markdown("""
**注意: **上传前请参考[**CSV示例**](https://raw.githubusercontent.com/thunderhit/cnsenti/master/test/cnsenti_example.csv)，将数据文件改为字段名为 **text**, 编码方式为 **UTF-8** 的 CSV 
    """)


@st.cache(suppress_st_warning=True)
def wordfreqs_count(uploaded_file='cnsenti_example.csv'):
    df = pd.read_csv(uploaded_file)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    text = ''.join(re.findall('[\u4e00-\u9fa5]+', ''.join(df['text'])))
    wordfreqs = dict()
    # for idx, text in enumerate(df['text']):
    words = jieba.lcut(text)
    wordset = set(words)
    for word in wordset:
        wordfreqs.setdefault(word, 0)
        wordfreqs[word] = wordfreqs[word] + words.count(word)
    res = [(k, v) for k, v in wordfreqs.items() if v > 1 and len(k) > 1]
    return res


def gen_wordcloud(wordfreqs):
    b = (WordCloud().add(series_name='WordCloud', data_pair=wordfreqs, word_size_range=[6, 66]).set_global_opts(
        title_opts=opts.TitleOpts(title="", title_textstyle_opts=opts.TextStyleOpts(font_size=23))))
    return st_pyecharts(b)


st.title('数据分析')
st.write('\n\n\n\n')
wc = st.button(label='词云图')
try:
    wordfreqs = wordfreqs_count(uploaded_file=uploaded_file)
except:
    wordfreqs = wordfreqs_count()
if wc:
    # st.balloons() 气球
    gen_wordcloud(wordfreqs=wordfreqs)


@st.cache(suppress_st_warning=True)
def measure(uploaded_file='cnsenti_example.csv'):
    df = pd.read_csv(uploaded_file)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    sentiment = Sentiment()
    emotion = Emotion()
    sensentiment_res = df['text'].apply(sentiment.sentiment_count).apply(pd.Series)
    emotion_res = df['text'].apply(emotion.emotion_count).apply(pd.Series)
    sentiment_result = pd.concat([df, sensentiment_res], axis=1)
    emotion_result = pd.concat([df, emotion_res], axis=1)
    return sentiment_result, emotion_result


senti = st.button(label='情感计算')
try:
    sentiment_result, emotion_result = measure(uploaded_file=uploaded_file)
except ValueError as e:
    sentiment_result, emotion_result = measure()
if senti:
    # st.balloons()
    st.markdown('**Sentiment Result**')
    st.write(sentiment_result)
    st.markdown('**Emoion Result**')
    st.write(emotion_result)

st.markdown("""
# 谢谢支持
- [**腾讯课堂: Python网络爬虫与文本分析**](https://ke.qq.com/course/482241?tuin=163164df)
- [**B站:大邓和他的python**](https://space.bilibili.com/122592901/channel/detail?cid=66008)
- [**github: DaDeng**](https://github.com/thunderhit)
- **公众号：大邓和他的python**
""")
# st.image('大邓和他的Python.png')

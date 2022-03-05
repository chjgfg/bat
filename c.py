import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
 
def sidebar():
    df_parameters = pd.DataFrame({'industry': ['-','金融','医疗'],'name': ['-','A','B'],'time': ['-','5天','7天']})
    select_parameters=[]
    option_industry = '-'
    option_name = '-'
    option_time = '-'
    
    option_industry = st.sidebar.selectbox('请选择股票行业',df_parameters['industry'])
    if option_industry != '-':
        select_parameters.append(option_industry)
        option_name = st.sidebar.selectbox('请选择股票名称',df_parameters['name'])
    else:
        pass
    
    if option_name!= '-':
        select_parameters.append(option_name)
        option_time = st.sidebar.selectbox('请选择时间窗口',df_parameters['time'])
    else:
        pass
        
    if option_time!= '-':
        select_parameters.append(option_time)
        version_option=st.sidebar.selectbox('选择历史版本：',('-','版本1', '版本2', '版本3'))
        st.sidebar.button('切换页面')
        st.sidebar.button('更新参数')
        
    return select_parameters
 
def display():
    st.set_option('deprecation.showPyplotGlobalUse', False)    
    #st.title(time.strftime("当前日期：%Y年%m月%d日", time.localtime()))
    start_date = "20200101"
    gap = 365
    date_list = pd.to_datetime(pd.date_range(start=start_date, periods=gap).strftime("%Y%m%d").tolist())
    chart_data = pd.DataFrame(np.random.randn(365, 2),columns=['真实值','预测值'],index=date_list)#传入DataFrame
    plt.plot(date_list,chart_data['真实值'],label='真实值') 
    plt.plot(date_list,chart_data['预测值'],label='预测值')
    plt.ylim(bottom=0)
    plt.xticks(rotation=45)
    plt.title(sidebar[0]+'行业'+sidebar[1]+'股票在'+sidebar[2]+'时间窗口下的预测结果',loc='center',fontproperties="SimHei",fontsize=20)
    plt.xlabel('日期',loc='right')
    plt.ylabel('价格',loc='top')
    plt.legend(loc='upper right')
    st.pyplot()
    
def button():
    ini_date=datetime.date.today()
    end_date=datetime.date.today()
    st.write('训练数据：')
    ini_date=st.date_input('起始日期：',value=datetime.date(2001,1,1))
    end_date=st.date_input('截止日期：') 
    st.button('确定')
    return ini_date,end_date
 
sidebar=sidebar()
#st.write(run)
if len(sidebar) != 3:
    st.header('请选择参数！')
else:
    display()
    button()
import pandas as pd 
import os
from sqlalchemy import create_engine
import psycopg2 
import io
## Data 불러오기 : Hn_ALL / HN_24_RC / 식품 음식 코드 목록 
DBengine = create_engine('postgresql://kbsraifl:l5Uu97h-9TUZr1vJMCh5_5wmyvT2u4Lz@isilo.db.elephantsql.com/kbsraifl')

for i in range(13,21):
    globals()['raw{}'.format(i)] =pd.read_spss(f'D:\codestates\Section3\Project 3\dataset\HN_ALL\HN{i}_ALL.sav')
    print(i)



def get_data(raw):
    import pandas as pd 
    from pandas.core.dtypes.dtypes import CategoricalDtype
    import numpy as np
    df=raw

    if df.year[0] >= 2019:
        diabetes = df.filter(regex ='HE_DM_HbA1c')# cate
        id = df.ID

    else:
        df.loc[df['HE_HbA1c']>= 5.7,'HE_DM_HbA1c'] =2
        df.loc[df['HE_HbA1c']>= 6.5,'HE_DM_HbA1c'] =3
        df.loc[df['HE_glu']>= 100,'HE_DM_HbA1c'] =2
        df.loc[df['HE_glu']>= 126,'HE_DM_HbA1c'] =3
        df.loc[df['HE_glu'].isnull(),'HE_DM_HbA1c'] =1
        df.loc[df['HE_HbA1c'].isnull(),'HE_DM_HbA1c'] =1
        df.loc[df['HE_glu'].isnull()==1,'HE_DM_HbA1c'] =np.NaN
        df.loc[df['HE_HbA1c'].isnull()==1,'HE_DM_HbA1c'] =np.NaN
        diabetes = df.filter(regex ='HE_DM_HbA1c')# cate
        id = df.id
    diabetes = df.filter(regex ='HE_DM_HbA1c')# cate
    diabetes =diabetes.replace(3,2)
    diabetes =diabetes.replace(np.NaN,1)


    diabetes=diabetes.astype('category')

    alchol1 = df.filter(regex ='BD1') # cate
    alchol1 =alchol1.astype('category')

    alchol2 = df.filter(regex ='BD2')
    obesity1 = df.filter(regex ='BO1') 
    obesity2 = df.filter(regex ='BO2')
    smoke1 =df.filter(regex ='BS1_')  # cate
    smoke1 =smoke1.astype('category')
    smoke2 =df.filter(regex ='BS2_')

    #smoke3 =df.filter(regex ='BS3_') # cate
    #smoke3=smoke3.drop(columns='BS3_3')
    #smoke3 =smoke3.astype('category')

    smoke4 =df.filter(regex ='BS6_2_1')
    #smoke5 =df.filter(regex ='BS5_4')
    if df.year[0] >= 2019:
        sleep1 = df.filter(regex ='(BP16_2)')*2
        sleep1 = sleep1.replace(99,np.NaN)
        sleep1 = sleep1.replace(88,np.NaN)

        sleep2 = df.filter(regex ='(BP16_1)')*5
        sleep2 = sleep2.replace(99,np.NaN)
        sleep2 = sleep2.replace(88,np.NaN)

        sleep3 = (sleep1.add(sleep2,fill_value=0))/7
        sleep = pd.DataFrame(sleep3.sum(axis=1), columns=['BP16'])
        sleep = sleep.replace(99,np.NaN)
    elif df.year[0] >= 2016:
        sleep1 = df.filter(regex ='Total_slp_wk')
        sleep1 = sleep1.replace(9999,np.NaN)
        sleep1 = sleep1.replace(8888,np.NaN)
        sleep1 =sleep1*2
        sleep2 = df.filter(regex ='Total_slp_wd')
        sleep2 = sleep2.replace(9999,np.NaN)
        sleep2 = sleep2.replace(8888,np.NaN)
        sleep2 =sleep2*5        
        sleep3 = (sleep1.add(sleep2,fill_value=0))/(7*60)
        sleep = pd.DataFrame(sleep3.sum(axis=1), columns=['BP16'])
        sleep = sleep.replace(99,np.NaN)
    elif df.year[0] >= 2010:
        sleep = pd.DataFrame(df.BP8, columns=['BP16']) 
        sleep = sleep.replace(99,np.NaN)
        sleep = sleep.replace(88,np.NaN)

    stress = df.BP1                   # cate
    stress=stress.astype('category')
    stress1 = df.filter(regex ='mh_stress') 

    if df.year[0] <= 2013:
        activity =df.filter(regex ='BE')

    else:
        activity =df.filter(regex ='BE')

    dia_family = df.filter(regex ='HE_DMfh')  # cate
    dia_family=dia_family.astype('category')
    blood_pre1= df.HE_sbp
    blood_pre2= df.HE_dbp
    #blood_pre3= df20.filter(regex ='HE_mPLS')

    height= df.filter(regex ='HE_ht')
    weight=df.HE_wt
    waistline = df.HE_wc
    BMI =  df.HE_BMI
    obesity =  df.filter(regex ='HE_obe') # cate
    obesity =  obesity.astype('category') 
    glucose = df.filter(regex ='HE_glu')
    HbA1 =  df.filter(regex ='HE_HbA1c')
    dietary1 = df.filter(regex ='L_BR_')
    dietary2 = df.filter(regex ='L_LN_')
    dietary3 = df.filter(regex ='L_DN_')
    dietary4 = df.filter(regex ='L_OUT')
    if df.year[0] >= 2016:
        Nutrient = df.filter(items =['N_INTK','N_EN','N_WATER','N_PROT','N_FAT','N_SFA','N_MUFA',
                                'N_PUFA','N_N3','N_N6','N_CHOL','N_CHO','N_TDF','N_SUGAR','N_CA',
                                'N_PHOS','N_FE','N_NA','N_K','N_VA_RAE', 'N_CAROT','N_RETIN',
                                'N_B1','N_B2','N_NIAC','N_FOLATE','N_VITC'])
    elif df.year[0] >= 2013:
        Nutrient = df.filter(items =['N_INTK','N_EN','N_WATER','N_PROT','N_FAT','N_SFA','N_MUFA',
                                'N_PUFA','N_N3','N_N6','N_CHOL','N_CHO','N_TDF','N_SUGAR','N_CA',
                                'N_PHOS','N_FE','N_NA','N_K','N_VA', 'N_CAROT','N_RETIN',
                                'N_B1','N_B2','N_NIAC','N_FOLATE','N_VITC'])
        Nutrient=Nutrient.rename(columns = {'N_VA':'N_VA_RAE'})



    insulin = df.filter(regex ='HE_insulin')


    df = pd.concat([diabetes,alchol1,alchol2,obesity1,obesity2,smoke1,smoke2,smoke4,
                sleep,stress,stress1,activity,dia_family,blood_pre1,blood_pre2,height,weight,waistline,
                BMI,obesity,glucose,HbA1,dietary1,dietary2,dietary3,dietary4,Nutrient],axis=1)

    return df


## 사용할 데이터 정리()
df13= get_data(raw13)
df14= get_data(raw14)
df15= get_data(raw15)
df16= get_data(raw16)
df17= get_data(raw17)
df18= get_data(raw18)
df19= get_data(raw19)
df20= get_data(raw20)

df = pd.concat([df13,df14,df15,df16,df17,df18,df19,df20],axis=0)
#df = df.dropna(axis=0, subset=['HE_DM_HbA1c'], inplace=False)


## Sending df to postgresql
df.to_sql('Diabetes_data', DBengine)
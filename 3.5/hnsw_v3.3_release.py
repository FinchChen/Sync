from japronto import Application

import fasttext
from sklearn import preprocessing
import nmslib
import pandas as pd
import jieba
import numpy as np

model_path = '/home/YifanChen/300d_to_100d.bin'
classifier = fasttext.load_model(model_path)

nms_model = nmslib.init(method='hnsw', space='cosinesimil')
nms_model.loadIndex(filename='10w_hnsw_v3.3.idx',load_data=False)

df_map = pd.read_csv('10w文库数据-原始.csv',encoding='utf8')

import jieba
filter_sentence = [
    '新华网|中新网|中国网|中经网|中广网|央视国际|凤凰网|中国教育电视台|中国视窗|国际在线|中国侨网|搜狐|新浪新闻首页纽国中国国际社会军事财经科技娱乐体坛世界华人中国之窗华新网视移民留学旅游地产商讯华社名人视点新闻首页-&gt;-&gt',
    '免责声明：本网为全球华人提供一个完全开放式的新闻资讯平台，任何单位或个人可自由在本网的相关栏目投稿、发布相关资讯或文章，网内所刊载的各类资讯p新闻、信息均来源于合作媒体或网友投稿发布，仅为广泛传播信息目的，本网不对其负有任何权利或责任。如有错误或侵权，请立即联系我们，我们会尽快更正或删除。本网站及论坛内所有资讯、新闻、信息均不代表本网观点。（浏览本网站，建议IE7.0以上版本显示分辨率1024*768）',
    '字体：【大中小】【繁体】',
    '意大利波兰华人资讯安哥拉华人网白俄罗斯华人网新加坡狮城网阿根廷华人在线柬埔寨中文社区匈牙利新导报国际日报日中新闻网神州时报澳洲中文汽车杂志中越快网在南非华人网乌克兰中文网波尔多华人网奋斗在西班牙非洲中文网新导报欧华网希中网德国开元网欧华传媒网中国移民网纽约在线美国新亚电视塔洲华人网美国华夏时报意大利移民网美国侨网千岛日报美国华星报美国华人在线纽约华人资讯网西班牙华人网聚华人唐人网今日悉尼奋斗在澳洲卡华网马达加斯加旅游网世界华人网巴西侨网南非华人网魁北克华人论坛安哥拉华人澳洲悠悠网缅甸中文网人民网华人频道青岛新闻网华商国际网中华时报网中国之窗辽宁新闻网鞍山大象网辽阳新闻网盐城新闻网襄阳新闻网海南网威海新闻网北京SO沈阳网西安新闻网杭州网大河网千龙网天津网哈尔滨新闻网龙虎网长沙新闻网北大华侨高管培训新西兰中华新闻通讯社NZCNA|联系我们|广告服务|隐私声明|版权声明|法律顾问|新西兰中华新闻网www.chinanews.co.nzCopyright2010-2012ChinaNews.Co.NZ(新闻资讯&amp;媒体平台)',
    'Tags：【来源】中华电视网【大中小】【打印】【关闭】【返回顶部】',
    '大信：冯雅各牧师证道（国粤双语）神使眼睛明亮：冯雅各牧师证道（国粤双语）我是全能神：冯雅各牧师证道（国粤双语）来，我们要敬拜耶和华：沃静芬姊妹证道（国粤・复活的大能：冯雅各牧师证道・妓女喇i哈：冯雅各牧师证道・得胜的信心：冯雅各牧师证道・恒心忍耐：冯雅各牧师证道・立定志向：冯雅各牧师证道奋斗在',
    '官方微信：imyixieshi本文链接:http://www.yixieshi.com/1126.html(转载请保留)',
    '【橙讯】',
    '亲，以上内容是否没有解决您的疑问，齐家装修专家团为您提供一对一的咨询服务（装修预算报价审核，户型改造建议，疑难杂症方案，材料购买详解，装修猫腻提醒），请添加微信号：qijia520321您也可以在微信中搜索”齐家网“论坛小程序，上千个装修专家，设计达人在线互动，装修疑难杂症，装修报价问题，户型改造问题在这里都能找到答案，快来看看别人家都怎么装修吧！',
    '来源丨猛哥（公众号ID：wm221x）作者丨猛哥头图丨',
    '――为买买买！卖卖卖！商家赚得新西兰圣诞新年长假过半7新西兰民防部：手机紧急警首届国际教育信息化大会在青岛举行尼泊尔留学生新西兰烛光悼念地震逝者中国留学生青岛华商会与新中两国交流与合作促进会牵手合作视频：海外“西藏梦”――专访新西兰藏文化研究视频：细心赢得一切――新西兰百伦移民留学顾问人物视频专访：专业态度，品质精神――奥克兰华新西兰青岛同乡会会员登记表新西兰华人家庭医生行骗案将继续审查待定处罚新西兰华裔男子利用留学生作掩护洗钱被判刑新西兰创业移民政策基本要求24小时图片点击排行新西兰侨胞感言买买买！卖卖卖新西兰圣诞新年新西兰民防部：新西兰Taranak新西兰湖南总商24小时视频点击排行i-SITE游客信息中心新西兰美酒佳肴罗托鲁瓦地区旅游宣传片新西兰-水上交通新西兰的毛利文化新西兰住宿-床位加早餐新西兰交通-道路信息新西兰毛利传说ManawatuNewZealandi-SITE游客信息中心视频：帆船之都―中国青岛EnglishEdition生命影音更多&gt;&gt;'
    
]    

def clean_article(sentence):
    
    for i in filter_sentence:
        sentence=sentence.replace(i,'')
    
    sentence = sentence.replace('\u3000','').replace(' ','').replace('\r','').replace('\ue0da','').replace('\n','').replace('|','')

    return sentence


from jieba import analyse
tfidf = analyse.extract_tags

def get_tfidf(content):
    kws1 = tfidf(content,topK=30,withWeight=True,withFlag=False)#,allowPOS=('ns','n','vn','v'))
    return kws1

def tmp_change(x):
    a = pd.DataFrame(x)
    return list(a[0]),list(a[1])

def get_word_matrix(x):
    tmp = []
    for i in x:
        tmp.append(classifier.get_word_vector(i))
    return np.array(tmp)


def tuijian(request, methods = ["POST"]):
    if request.method == "POST" and 'content' in request.form:

        sentence_to_predict = clean_article(request.form['content'])

        a = get_tfidf(sentence_to_predict)

        x,y = tmp_change(a)

        word_matrixs = get_word_matrix(x)

        word_weights = np.array(y)

        m3 = word_matrixs * np.transpose(word_weights * np.ones((100,word_matrixs.shape[0])))

        ave = np.sum(m3,axis=0)/(m3.shape[0]+1)

        inputvec = preprocessing.normalize([ave,], norm='l2')[0]

        ids, distances = nms_model.knnQuery(inputvec, k=5)

        dict1 = dict([([1,2,3,4,5][i],{'prob':1-(distances[i]),'_id':df_map['_id'][ids[i]]}) for i in range(5)])
        
        if 'show_article' in request.form:
            
            if request.form['show_article'] == 'yes':
                dict1 = dict([([1,2,3,4,5,6][i],{'prob':1-(distances[i]),'_id':df_map['_id'][ids[i]],'title':df_map['title'][ids[i]],'content':df_map['content'][ids[i]]}) for i in range(5)])    
                
        return request.Response(json=dict1)

    return request.Response(text='穿山甲到底说了什么?')


app = Application()
app.router.add_route('/tuijian', tuijian)
app.run(host='127.0.0.1',port=14593,debug=True)

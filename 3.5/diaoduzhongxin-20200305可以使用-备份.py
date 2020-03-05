from japronto import Application

import requests
from elasticsearch import Elasticsearch

import redis
import hashlib

es = Elasticsearch()
redis1 = redis.Redis(host='127.0.0.1', port= 6379, db= 0)

test = {
  "query": {
    "script_score": {
      "min_score":0.6,
      "query" : {
        "match_all":{}
      },
      "script": {
        "source": "1 / (1 + l2norm(params.query_vector, 'my_dense_vector'))",
        "params": {
          "query_vector": [0.3076026, 0.40158343, 0.037472293, -0.023448404, -0.12641075, 0.18784791, -0.22594255, 0.042800742999999995, -0.14818178, -0.13573748, -0.15438777, 0.014563712, -0.024950476, -0.075634435, -0.16084047, 0.10481286, 0.18689136, 0.13004917, -0.069410935, 0.00044900647, 0.0098925745, -0.001807725, -0.19068593, 0.021637137999999997, -0.056592292999999995, -0.018035665, -0.070357904, -0.048465688, 0.11511488, 0.19348082, 0.16334033, 0.06447884400000001, 0.13016757, -0.019691806, -0.020191489, 0.015546986, 0.031684965, -0.04817288, -0.06248542, -0.054339767000000004, -0.027172348, -0.017456198, 0.040579844, -0.056884732, -0.09429286, 0.087917544, -0.28769276, 0.09087726, 0.05476374, 0.011553496000000002, -0.11633229, -0.07471947, -0.12266219, 0.097280584, 0.012712383999999998, -0.015457037, -0.02545418, 0.04847752, -0.014195667, 0.012362796, 0.04001723, -0.026509017000000003, 0.052133884000000005, 0.0058652977, -0.07400676, -0.0025838283, 0.10580598, 0.058501642, 0.059161194, 0.055182445999999996, 0.0113331415, -0.13906446, 0.02365516, -0.036346737000000004, 0.019930536000000002, 0.01762282, 0.033885233, -0.007897217, -0.043617174, 0.017600946, 0.10539335, 0.02769088, 0.083795846, 0.16449027, -0.07043237, -0.058462687, -0.09188373400000001, 0.09111979, -0.030251188, -0.031871617000000005, -0.06262229400000001, 0.111787595, -0.003931845, -0.033218138, -0.020982424, -0.004300374, 0.02898827, 7.41621e-05, -0.052188545, 0.021084705]
        }
      }
    }
  },
  "from":0,
  "size":500
}


def md5(txt): # 以空格分隔 #针对于content是关键词的情况

    tmp_list=[]
    tmp_str=''
    for keyword in txt.strip(' ').replace('  ',' ').split(' '):
        a = hashlib.md5(keyword.encode("utf-8")).hexdigest()
        tmp_list.append(a)
    
    for i in sorted(tmp_list):
        tmp_str += i

    m = hashlib.md5(tmp_str.encode("utf-8"))

    return m.hexdigest()


def tuijian(request, methods = ["POST"]):
    if request.method == "POST" and 'content' in request.form and 'user_id' in request.form and 'size' in request.form:

        raw_content = request.form['content']
        user_id = request.form['user_id']
        
        return_size = int(request.form['size'])
        if return_size > 50:
            return_size = 50
        
        rec_list = []
        md5_content = md5(raw_content)

        pipe = redis1.pipeline()
        

        if not redis1.exists(user_id+md5_content): # 如果没有缓存就从es抓

            try:

                tmp_dict = {'content':raw_content}

                content_vec = requests.post(url='http://127.0.0.1/vectorize/v3.4',data=tmp_dict,timeout=1).json()
                #给自己的向量化api

                test['query']['script_score']['script']['params']['query_vector'] = content_vec['vec']

                res = es.search(index="tuijian_v3.3", body=test)

                #返回结果太少怎么办?

                r1 = res['hits']['hits']

                tmp_dict = {}
            
                for i in range(len(r1)):
                    tmp_dict[r1[i]['_id']] = r1[i]['_score']    

                for i in tmp_dict.keys():
                    pipe.execute_command('bf.exists',user_id+'_bloom',i)
            
                tmp_result = pipe.execute()

                if not 0 in tmp_result: #全被推荐过了

                    return_dict = {'status':601,
                            'info':'内容库中已经没有未推荐过的内容了','data':['']}

                    return request.Response(json=return_dict)


                redis1.zadd(user_id+md5_content,tmp_dict)
                #redis1.expire(user_id+md5_content,
            
            except requests.exceptions.Timeout:

                rec_list = ['12345678']# 指定热门推荐api

                return_dict = {'status':602,
                            'info':'向量化api超时(1s),返回热门内容,热门内容待指定',
                            'data':rec_list}

                return request.Response(json=return_dict)


        try:

            tmp1 = redis1.zrange(user_id+md5_content,0,50,False,False,float) # 默认给回前50个 #没有50个会不会报错? 不会报错

            for i in tmp1:
                tmp_i = i.decode('utf8')
                rec_list.append(tmp_i)
                pipe.execute_command('bf.exists',user_id+'_bloom',tmp_i)
            
            tmp_result = pipe.execute() # 判断是否已推荐 100个花费3ms左右

            if 1 in tmp_result:

                for i in range(tmp_result.count(1)):

                    a = tmp_result.index(1)

                    pipe.zrem(user_id+md5_content,rec_list[a]) #redis库去除历史已推荐

                    tmp_result.pop(a)
                    rec_list.pop(a) #rec_list去除已推荐

                pipe.execute()
            
            if len(rec_list) >= return_size:
                rec_list = rec_list[:return_size] #保留前n个
            
        except Exception as e:

            print(e)
            return_dict = {'status':610,'info':e,'data':['']}
            return request.Response(json=return_dict)

        
        if len(rec_list)>0: 
        
            for i in rec_list:
                pipe.execute_command('bf.add',user_id+'_bloom',i)

            tmp_result = pipe.execute() # 给进布隆过滤器
            
            redis1.zremrangebyrank(user_id+md5_content, 0, return_size-1) # 已返回的就从redis表中移除
        
        #print(rec_list)

        return_dict = {'status':200,
                    'info':'success',
                    'data':rec_list}

        return request.Response(json=return_dict)

    return request.Response(text='穿山甲到底说了什么?')


app = Application()
app.router.add_route('/tuijian/v3.4', tuijian)
app.run(host='127.0.0.1',port=14593,debug=True)

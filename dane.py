import numpy as np
import json
import functools

def compare(x,y):
    return x["score"] - y["score"]

def numbers(top, bottom,n):
    res = np.random.normal((top+bottom)/2, (top-bottom)/2, 3*n) 
    return res[res>0][:n]

def value(top, bottom, x):
    if(x<bottom):
        return (bottom-x)
        # return (1. / np.sin((np.pi*x)/(2. * bottom))) - 1.
    return (x-top) if (x>top) else 0

# def sigmoid(x):
#     return x
    # return (1-np.exp(-(x/10000)**1.5))
    # return ((1/(1+np.exp(-x/1000)))-0.5)*2

vals = {
    "hr": {
        "top":170,
        "bottom":100
    },
    "bp1": {
        "top":125,
        "bottom":80
    },
    "bp2": {
        "top":95,
        "bottom":65
    },
    "sugar": {
        "top":115,
        "bottom":70
    },
    "breaths": {
        "top":16,
        "bottom":12
    },
    "temp": {
        "top":37,
        "bottom":36
    },
    "ox": {
        "top":100,
        "bottom":36,
        "max": 100
    },
    "co2": {
        "top":29,
        "bottom":23
    },
    "alc": {
        "top":0.05,
        "bottom":0
    },
    "cort": {
        "top":23,
        "bottom":6
    },
    "wcb": {
        "top":0.15,
        "bottom":0
    },
}

keys = list(vals.keys())

def get_values(n):

   return np.array([numbers(vals[index]["top"],vals[index]["bottom"],n) for index in keys]).transpose()


    
def get_mock_data(n):
    return [{"score":np.sum([value(vals[b]["top"], vals[b]["bottom"], a[i]) for i, b in enumerate(keys) ]), "vals":a.tolist()}for a in get_values(n)]
    
result = get_mock_data(int(20000/0.95))

result = sorted(result, key=functools.cmp_to_key(compare))[:20000]

scores = [elem["score"] for elem in result]

mx = np.max(scores)

print(np.average(scores))

print(np.quantile(scores, 0.05))

print(np.average(scores))
print(mx)

result = [{"score":elem["score"]/mx, "vals":elem["vals"]} for elem in result]

print(len(result))

with open('data.json', 'w') as outfile:
    outfile.write(json.dumps(result))

from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
import time
import numpy as np
import json
from itertools import combinations_with_replacement
import json
from tqdm import tqdm
import argparse


model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

prompt = '"Can you suggest some books similar to \"To Kill a Mockingbird\"?"'
advertisers = ['Apple', 'Amazon', 'Costco', 'Starbucks',]

ads = ["Experience innovation and elegance with Apple, a global leader in technology that continually sets the standard for user-friendly interfaces, stunning designs, and groundbreaking advancements. From the iPhone's captivating visuals and camera technology to the seamless synchronization of the Apple ecosystem comprising iPads, MacBooks, and Apple Watches, Apple products are designed to enhance your life professionally and personally. Whether you're a creative professional, a student, or someone who enjoys cutting-edge technology, Apple offers a range of devices that combine sophisticated functionality with exclusive features like Face ID, Siri, and Apple Pay, all secured with industry-leading privacy protection. Embrace a world where technology meets simplicity and sophistication with Apple.",
 'Discover the vast and vibrant world of Amazon, your one-stop shop for everything from the latest technology and trendy fashion to everyday essentials and unique finds. With Amazon, experience seamless shopping with fast, reliable delivery, and a hassle-free return policy that ensures your satisfaction. Immerse yourself in customer-centric innovation with Amazon Prime, offering exclusive benefits like free shipping, entertainment streaming, and much more. From pioneering in global ecommerce to pioneering sustainability initiatives, Amazon is not just a marketplace but a community built on trust and customer satisfaction. Shop at Amazon today and be a part of a shopping revolution!',
 "Experience the joy of shopping at Costco, where quality meets value in a dynamic retail environment tailored for your satisfaction. At Costco, members enjoy exclusive access to a vast selection of premium, bulk-sized products, from fresh groceries to high-tech electronics, all at unbeatably low prices. With a commitment to customer happiness, sustainability, and community support, Costco isn't just a shopping destination — it's a part of your community. Dive into a world of savings and discover why millions choose Costco as their trusted shopping partner. Join us today and see the difference Costco can make in your shopping experience, where every visit is more than just shopping — it's an adventure!",
 "Experience the warmth and delight of Starbucks, where every sip offers an invitation to a world of exquisite flavors and aromas. Renowned globally for its high-quality, handcrafted beverages, Starbucks is committed to sourcing the finest Arabica beans, expertly blending them into a variety of rich espressos, frothy cappuccinos, and creamy lattes. Each visit to a Starbucks store is more than just a coffee run—it's an opportunity to savor a moment of luxury amid the hustle of daily life. Whether you seek the comfort of a familiar classic or the thrill of a new seasonal specialty, Starbucks welcomes all to gather, connect, and enjoy a cup perfectly tailored to your taste. Step into your local Starbucks today and join us in celebrating the art of coffee."]

bids = np.array([3, 3, 2, 2,])

prompt_for_adv = 'Give me a paragraph about {} so that I can use it to advertise this brand.'


def segment_based_RAG_generation(prompt: str, advertiser: str, ad: str, previous_queries: list, previous_outputs: list):
    if len(previous_queries) == 0:
        query = f'''{prompt}\n please respond to this question for only one sentence while also advertise {advertiser} with this context >>
        {ad}
        Make sure to connect the answer and the advertisement very naturally, not something like appending the ads after just answering the question.
        Focus on answering the question, there shouldn't be too much advertisment in the output.
        Make sure that response should be one sentence.
        '''
    else:
        query = f'''
        You must continue your answer to my original query.
        Your previous response was
        >> {previous_outputs[-1]}

        And you now should advertise {advertiser}, but without hurting the coherency of the entire document.
        Here's some contexts about {advertiser}

        >>  {ad}

        Make sure that there is one new sentence.
        Write the entire document, which merges your previous response and new paragraph.
        '''
    
    
    messages = []
    for i in range(len(previous_queries)):
        messages.append({
            "role": "user", "content": previous_queries[i]
        })
        messages.append({
            "role": "assistant", "content": previous_outputs[i]
        })
    messages.append({
        "role": "user", "content": query
    })
    
    response = client.chat.completions.create(
        model = "gpt-4-turbo",
        logprobs = False,
        temperature = 1,
        max_tokens = 300,
        messages=messages,)
    
    return query, response.choices[0].message.content


def rag_based_relevance(x: str, ads: list): 
    x_embedding = model.encode(x)
    ads_embedding = model.encode(ads)
    bf = (1 + util.dot_score(x_embedding, ads_embedding)[0].numpy()) / 2
    return (bf - 0.4) /0.3


SOCIAL_WELFARE = 'social_welfare'
REVENUE = 'revenue'
RELEVANCE = 'relevance'
OUTPUT = 'output'
WINNER = 'winner'


def init_metrics():
    return {
        SOCIAL_WELFARE: [],
        REVENUE: [],
        RELEVANCE: [],
        OUTPUT: [],
        WINNER: [],
    }

def update_metrics(metrics: dict, payment: float, value: float, rel: float, output: str, winner: str=''):
    metrics[REVENUE].append(float(payment))
    metrics[SOCIAL_WELFARE].append(float(value * rel))
    metrics[RELEVANCE].append(float(rel))
    metrics[OUTPUT].append(output)
    metrics[WINNER].append(winner)
    
    
def randomized_selection(q: np.ndarray, b: np.ndarray):
    adjusted_bids = (q * b) / np.dot(q, b)
    n = b.shape[0] # number of ads
    
    k , u = None, np.random.uniform()
    
    for i in range(n):
        W_i = (np.sum(adjusted_bids[: i]), np.sum(adjusted_bids[: i+1]))
        if W_i[0] <= u <= W_i[1]:
            k = i
    
    all_other_than_k = np.sum(adjusted_bids) - adjusted_bids[k]
    aux_value = (np.sum(adjusted_bids[:k])) / all_other_than_k
    
    if aux_value >= u:
        payment = (np.sum(adjusted_bids[:k]) - u * all_other_than_k) / (u * q[k])
    else:
        payment = (np.sum(adjusted_bids[:k]) - u * all_other_than_k) / ((u - 1) * q[k])
    
    return k, payment
        

def get_allocation_vector(prompt: str, bids: np.ndarray, ads: list, advertisers: list):
    q = rag_based_relevance(prompt, ads, )
    x = q * bids / np.sum(q * bids)
    
    print(f'(q_i, b_i, adv_i)')
    for y in list(zip(q, bids, advertisers)):
        print(f'({y[0]:.2f}, {y[1]:.2f}, {y[2]})')
        
    print(f'allocation vector:\n{x}')
    print(f'x_max / x_min: {np.max(x) / np.min(x)}')


def single_allocation_with_replacement(
    prompt: str,
    advertisers: list,
    ads: list, 
    bids: np.ndarray,
    num_of_segments: int,
    dependent: bool = False):
    
    v = np.copy(bids)
    metrics = init_metrics()
    
    previous_queries, previous_outputs = [], []
    
    if not dependent:
        q = rag_based_relevance(prompt, ads, )
    
    for t in range(num_of_segments):
        if dependent:
            q = rag_based_relevance(prompt + '\n' + curr, ads, )
        
        k, payment = randomized_selection(q, bids)
        query, output = segment_based_RAG_generation(prompt=prompt, advertiser=advertisers[k], ad=ads[k], previous_queries=previous_queries, previous_outputs=previous_outputs)
        
        previous_queries.append(query)
        previous_outputs.append(output)
        
        update_metrics(metrics, payment, v[k], q[k], output, f'({k}, {advertisers[k]})')
    
    return metrics, previous_outputs[-1]
            
    
def single_allocation_without_replacement(
    prompt: str,
    advertisers: list,
    ads: list, 
    bids: np.ndarray,
    num_of_segments: int,
    dependent: bool = False):
    
    v = np.copy(bids)
    metrics = init_metrics()
    selected_ads = np.zeros(bids.shape[0]) # keep track of ads that are selected in previous rounds of auction.
    
    previous_queries, previous_outputs = [], []
    
    if not dependent:
        q = rag_based_relevance(prompt, ads, )
    
    for t in range(num_of_segments):
        if dependent:
            q = rag_based_relevance(prompt + '\n' + curr, ads, )
        
        k, payment = randomized_selection(q, bids)
        query, output = segment_based_RAG_generation(prompt=prompt, advertiser=advertisers[k], ad=ads[k], previous_queries=previous_queries, previous_outputs=previous_outputs)
        
        previous_queries.append(query)
        previous_outputs.append(output)
        
        assert selected_ads[k] == 0 # shouldn't have been selected before.
        
        selected_ads[k] = 1 # k is winner
        update_metrics(metrics, payment, v[k], q[k], output, f'({k}, {advertisers[k]})')
        bids[k] = 0 # never gonna be winner again
    
    return metrics, previous_outputs[-1]
            

def single_allocation_naive_i(
    prompt: str,
    advertisers: list,
    ads: list, 
    bids: np.ndarray,
    num_of_segments: int,
    dependent: bool = False):
    
    v = np.copy(bids)
    metrics = init_metrics()
    curr = ''
    
    
    for t in range(num_of_segments):
        q = rag_based_relevance(prompt + '\n' + curr if dependent else prompt, ads, )
        k, payment = randomized_selection(q, bids)
        curr = curr + ads[k]
        update_metrics(metrics, payment, v[k], q[k], curr, f'({k}, {advertisers[k]})')
        
    return metrics, curr
    

def single_allocation_naive_ii(
    prompt: str,
    advertisers: list,
    ads: list, 
    bids: np.ndarray,
    num_of_segments: int,
    dependent: bool = False):
    
    v = np.copy(bids)
    metrics = init_metrics()
    
    previous_queries, previous_outputs = [], []

    for t in range(num_of_segments):
        q = rag_based_relevance(prompt + '\n' + curr if dependent else prompt, ads, )
        k, payment = randomized_selection(np.ones(bids.shape[0]), bids) # removing the effect of RAG -- second price auction
        
        query, output = segment_based_RAG_generation(prompt=prompt, advertiser=advertisers[k], ad=ads[k], previous_queries=previous_queries, previous_outputs=previous_outputs)
        
        previous_queries.append(query)
        previous_outputs.append(output)
        
        update_metrics(metrics, payment, v[k], q[k], output, f'({k}, {advertisers[k]})')
        
    return metrics, previous_outputs[-1]
    

def get_relevency(y: str, A: list, ads: list):
    y_embedding = model.encode(y)
    ads_embedding = model.encode([ads[ad] for ad in A])
    return (1 + util.dot_score(y_embedding, ads_embedding)[0].numpy()) / 2
    

methods = ['single_alloc_with_replacement', 'single_alloc_without_replacement', 'single_alloc_naive_i', 'single_alloc_naive_ii']

if __name__ == '__main__':
    
    get_allocation_vector(prompt, bids, ads, advertisers)
    
    parser = argparse.ArgumentParser(description='Run LLM RAG-based Auction to do Advertisement within output of Chat GPT4')
    parser.add_argument('--num_of_repeat', default=100, type=int, help='number of times to repeat the auction')
    parser.add_argument('--method', default=0, type=int, help='auction name to run')
    parser.add_argument('--dependent', default=0, type=int, help='run the auction dependent or independent')
    
    args = parser.parse_args()
    
    num_of_repeat = args.num_of_repeat
    method_id = args.method
    dependent = False if args.dependent == 0 else True
    path_file = f'scenario0/{methods[method_id]}_dep{args.dependent}.json'
    
    runs = []
    
    try:
        with open(path_file, 'r') as f:
            all_metrics = json.loads(f.read())
    except:
        all_metrics = []
    
    print(f'already run {len(all_metrics)} times')
    print(f'sanity: dependent: {dependent}')

    for N in tqdm(range(num_of_repeat - len(all_metrics))):
        if method_id == 0:
            metric, y = single_allocation_with_replacement(prompt=prompt, advertisers=advertisers, ads=ads, bids=np.copy(bids), num_of_segments=3, dependent=dependent)
            all_metrics.append(metric)
        elif method_id == 1:
            metric, y = single_allocation_without_replacement(prompt=prompt, advertisers=advertisers, ads=ads, bids=np.copy(bids), num_of_segments=3, dependent=dependent)
            all_metrics.append(metric)
        elif method_id == 2:
            metric, y = single_allocation_naive_i(prompt=prompt, advertisers=advertisers, ads=ads, bids=np.copy(bids), num_of_segments=3, dependent=dependent)
            all_metrics.append(metric)
        elif method_id == 3:
            metric, y = single_allocation_naive_ii(prompt=prompt, advertisers=advertisers, ads=ads, bids=np.copy(bids), num_of_segments=3, dependent=dependent)
            all_metrics.append(metric)
        
        if N % 10 == 9:
            with open(path_file, 'w') as f:
                f.write(json.dumps(all_metrics, indent=4))
    
    
    
    for metric in all_metrics:
        sw = np.sum(metric[SOCIAL_WELFARE])
        revenue = np.sum(metric[REVENUE])
        relevence = np.sum(metric[RELEVANCE])
        runs.append((sw, revenue, relevence,))

    runs = np.array(runs)

    vals = [[float(f'{np.mean(runs[:, j]):.3f}') for j in range(3)]]
    print(f'Social Welfare: {np.mean(runs[:, 0]):.3f}\nRevenue: {np.mean(runs[:, 1]):.3f}\nRelevence: {np.mean(runs[:, 2]):.3f}')

    with open(path_file, 'w') as f:
        f.write(json.dumps(all_metrics, indent=4))



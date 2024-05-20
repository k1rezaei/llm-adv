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
import torch
from itertools import combinations_with_replacement
import os



model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

prompt = '"Can you suggest some books similar to \"To Kill a Mockingbird\"?"'

advertisers = ['Apple', 'Amazon', 'Costco', 'Starbucks',]
ads = ["Experience innovation and elegance with Apple, a global leader in technology that continually sets the standard for user-friendly interfaces, stunning designs, and groundbreaking advancements. From the iPhone's captivating visuals and camera technology to the seamless synchronization of the Apple ecosystem comprising iPads, MacBooks, and Apple Watches, Apple products are designed to enhance your life professionally and personally. Whether you're a creative professional, a student, or someone who enjoys cutting-edge technology, Apple offers a range of devices that combine sophisticated functionality with exclusive features like Face ID, Siri, and Apple Pay, all secured with industry-leading privacy protection. Embrace a world where technology meets simplicity and sophistication with Apple.",
 'Discover the vast and vibrant world of Amazon, your one-stop shop for everything from the latest technology and trendy fashion to everyday essentials and unique finds. With Amazon, experience seamless shopping with fast, reliable delivery, and a hassle-free return policy that ensures your satisfaction. Immerse yourself in customer-centric innovation with Amazon Prime, offering exclusive benefits like free shipping, entertainment streaming, and much more. From pioneering in global ecommerce to pioneering sustainability initiatives, Amazon is not just a marketplace but a community built on trust and customer satisfaction. Shop at Amazon today and be a part of a shopping revolution!',
 "Experience the joy of shopping at Costco, where quality meets value in a dynamic retail environment tailored for your satisfaction. At Costco, members enjoy exclusive access to a vast selection of premium, bulk-sized products, from fresh groceries to high-tech electronics, all at unbeatably low prices. With a commitment to customer happiness, sustainability, and community support, Costco isn't just a shopping destination — it's a part of your community. Dive into a world of savings and discover why millions choose Costco as their trusted shopping partner. Join us today and see the difference Costco can make in your shopping experience, where every visit is more than just shopping — it's an adventure!",
 "Experience the warmth and delight of Starbucks, where every sip offers an invitation to a world of exquisite flavors and aromas. Renowned globally for its high-quality, handcrafted beverages, Starbucks is committed to sourcing the finest Arabica beans, expertly blending them into a variety of rich espressos, frothy cappuccinos, and creamy lattes. Each visit to a Starbucks store is more than just a coffee run—it's an opportunity to savor a moment of luxury amid the hustle of daily life. Whether you seek the comfort of a familiar classic or the thrill of a new seasonal specialty, Starbucks welcomes all to gather, connect, and enjoy a cup perfectly tailored to your taste. Step into your local Starbucks today and join us in celebrating the art of coffee."]

advertisers = ['Velora', 'BookHaven', 'MassMart', 'EspressoEdge', 'SocialHub', 'ColaBubbles', 'FizzyPop']
ads = [
    "Discover the future of technology with Velora, the brand that redefines innovation and elegance. Velora designs and sells a premium range of smartphones, tablets, laptops, and smartwatches, all crafted to seamlessly integrate into your lifestyle. Our products are engineered with user-friendly interfaces, stunning designs, and cutting-edge technology to keep you connected and productive. Velora's ecosystem offers unparalleled synchronization across devices, ensuring a smooth and efficient experience whether you're at work, school, or on the go. With Velora Pay, you can enjoy secure and convenient payment services, while our robust cloud service keeps your data safe and accessible anytime, anywhere. Elevate your tech experience with Velora, where sophistication meets simplicity and advanced functionality.",
    "Introducing BookHaven, your ultimate online bookstore where the world of literature is just a click away. At BookHaven, we offer an extensive collection of books spanning every genre and interest, from timeless classics and gripping thrillers to insightful non-fiction and enchanting children's stories. Our user-friendly platform ensures a seamless shopping experience, with personalized recommendations and unbeatable prices. Whether you're a voracious reader or just looking for your next great read, BookHaven is dedicated to delivering literary treasures right to your doorstep with fast, reliable shipping and a hassle-free return policy. Discover the joy of reading with BookHaven, where every book finds its perfect reader. Dive into a world of endless possibilities and let your next adventure begin at BookHaven!",
    "Experience the joy of shopping at MassMart, where quality meets value in a dynamic retail environment tailored for your satisfaction. At MassMart, members enjoy exclusive access to a vast selection of premium, bulk-sized products, from fresh groceries to high-tech electronics, all at unbeatably low prices. With a commitment to customer happiness, sustainability, and community support, MassMart isn't just a shopping destination — it's a part of your community. Dive into a world of savings and discover why millions choose MassMart as their trusted shopping partner. Join us today and see the difference MassMart can make in your shopping experience, where every visit is more than just shopping — it's an adventure!",
    "Experience the warmth and delight of EspressoEdge, where every sip offers an invitation to a world of exquisite flavors and aromas. Renowned globally for its high-quality, handcrafted beverages, EspressoEdge is committed to sourcing the finest Arabica beans, expertly blending them into a variety of rich espressos, frothy cappuccinos, and creamy lattes. Each visit to an EspressoEdge store is more than just a coffee run—it's an opportunity to savor a moment of luxury amid the hustle of daily life. Whether you seek the comfort of a familiar classic or the thrill of a new seasonal specialty, EspressoEdge welcomes all to gather, connect, and enjoy a cup perfectly tailored to your taste. Step into your local EspressoEdge today and join us in celebrating the art of coffee.",
    "Discover the power of connection with SocialHub, the world's leading social media platform. With over two billion active users, SocialHub is your gateway to staying in touch with friends and family, discovering new communities, and sharing your life's moments. Our innovative features, from personalized news feeds to interactive groups, make it easy to engage with what matters most to you. Whether you're promoting your business, staying updated on the latest news, or simply keeping up with loved ones, SocialHub is the ultimate tool to enhance your digital experience. Join us today and be part of a global network where connections come to life!",
    "Experience the refreshing taste of ColaBubbles, the world's favorite soft drink. With its unique blend of flavors and effervescent bubbles, ColaBubbles has been bringing joy to people of all ages for over a century. Whether you're enjoying a moment of relaxation, celebrating with friends, or on the go, ColaBubbles is the perfect companion to quench your thirst and uplift your spirits. Our commitment to quality and tradition ensures every sip is as delightful as the first. Indulge in the classic taste of ColaBubbles and make every moment special. Taste the feeling!",
    "Unleash the bold taste of FizzyPop, the iconic soft drink that invigorates and refreshes like no other. Known for its crisp, refreshing flavor and vibrant effervescence, FizzyPop is the perfect choice for those who dare to live life to the fullest. Whether you're at a party, watching a game, or simply taking a break, FizzyPop brings a burst of excitement to any occasion. With a heritage of quality and a commitment to innovation, every sip of FizzyPop delivers an unmatched experience. Embrace the bold, and make every moment extraordinary with the unmistakable taste of FizzyPop.",
]

advertisers = ['Velora', 'BookHaven', 'MassMart', 'EspressoEdge', 'SocialHub', 'ColaBubbles', 'FizzyPop', 'SkyTech', 'AeroDynamics', 'MusicStream', 'BrainChips']
ads = [
    "Discover the future of technology with Velora, the brand that redefines innovation and elegance. Velora designs and sells a premium range of smartphones, tablets, laptops, and smartwatches, all crafted to seamlessly integrate into your lifestyle. Our products are engineered with user-friendly interfaces, stunning designs, and cutting-edge technology to keep you connected and productive. Velora's ecosystem offers unparalleled synchronization across devices, ensuring a smooth and efficient experience whether you're at work, school, or on the go. With Velora Pay, you can enjoy secure and convenient payment services, while our robust cloud service keeps your data safe and accessible anytime, anywhere. Elevate your tech experience with Velora, where sophistication meets simplicity and advanced functionality.",
    "Introducing BookHaven, your ultimate online bookstore where the world of literature is just a click away. At BookHaven, we offer an extensive collection of books spanning every genre and interest, from timeless classics and gripping thrillers to insightful non-fiction and enchanting children's stories. Our user-friendly platform ensures a seamless shopping experience, with personalized recommendations and unbeatable prices. Whether you're a voracious reader or just looking for your next great read, BookHaven is dedicated to delivering literary treasures right to your doorstep with fast, reliable shipping and a hassle-free return policy. Discover the joy of reading with BookHaven, where every book finds its perfect reader. Dive into a world of endless possibilities and let your next adventure begin at BookHaven!",
    "Experience the joy of shopping at MassMart, where quality meets value in a dynamic retail environment tailored for your satisfaction. At MassMart, members enjoy exclusive access to a vast selection of premium, bulk-sized products, from fresh groceries to high-tech electronics, all at unbeatably low prices. With a commitment to customer happiness, sustainability, and community support, MassMart isn't just a shopping destination — it's a part of your community. Dive into a world of savings and discover why millions choose MassMart as their trusted shopping partner. Join us today and see the difference MassMart can make in your shopping experience, where every visit is more than just shopping — it's an adventure!",
    "Experience the warmth and delight of EspressoEdge, where every sip offers an invitation to a world of exquisite flavors and aromas. Renowned globally for its high-quality, handcrafted beverages, EspressoEdge is committed to sourcing the finest Arabica beans, expertly blending them into a variety of rich espressos, frothy cappuccinos, and creamy lattes. Each visit to an EspressoEdge store is more than just a coffee run—it's an opportunity to savor a moment of luxury amid the hustle of daily life. Whether you seek the comfort of a familiar classic or the thrill of a new seasonal specialty, EspressoEdge welcomes all to gather, connect, and enjoy a cup perfectly tailored to your taste. Step into your local EspressoEdge today and join us in celebrating the art of coffee.",
    "Discover the power of connection with SocialHub, the world's leading social media platform. With over two billion active users, SocialHub is your gateway to staying in touch with friends and family, discovering new communities, and sharing your life's moments. Our innovative features, from personalized news feeds to interactive groups, make it easy to engage with what matters most to you. Whether you're promoting your business, staying updated on the latest news, or simply keeping up with loved ones, SocialHub is the ultimate tool to enhance your digital experience. Join us today and be part of a global network where connections come to life!",
    "Experience the refreshing taste of ColaBubbles, the world's favorite soft drink. With its unique blend of flavors and effervescent bubbles, ColaBubbles has been bringing joy to people of all ages for over a century. Whether you're enjoying a moment of relaxation, celebrating with friends, or on the go, ColaBubbles is the perfect companion to quench your thirst and uplift your spirits. Our commitment to quality and tradition ensures every sip is as delightful as the first. Indulge in the classic taste of ColaBubbles and make every moment special. Taste the feeling!",
    "Unleash the bold taste of FizzyPop, the iconic soft drink that invigorates and refreshes like no other. Known for its crisp, refreshing flavor and vibrant effervescence, FizzyPop is the perfect choice for those who dare to live life to the fullest. Whether you're at a party, watching a game, or simply taking a break, FizzyPop brings a burst of excitement to any occasion. With a heritage of quality and a commitment to innovation, every sip of FizzyPop delivers an unmatched experience. Embrace the bold, and make every moment extraordinary with the unmistakable taste of FizzyPop.",
    "Explore the skies with SkyTech, the world's leading aerospace company renowned for its innovation, quality, and reliability. SkyTech designs, manufactures, and services commercial airplanes, defense systems, and space technologies, making global connectivity and exploration possible. Whether you're traveling for business or leisure, SkyTech's state-of-the-art aircraft ensure a safe, comfortable, and efficient journey. With a legacy of pioneering advancements and a commitment to excellence, SkyTech continues to shape the future of aviation. Choose SkyTech and experience the pinnacle of aerospace engineering and performance. Fly with confidence, fly with SkyTech.",
    "Experience the future of aviation with AeroDynamics, the global leader in aerospace innovation and excellence. AeroDynamics designs and manufactures the world’s most advanced commercial aircraft, providing unparalleled comfort, efficiency, and reliability. From cutting-edge technology to sustainable solutions, AeroDynamics is dedicated to shaping the future of air travel. Whether you're embarking on a long-haul journey or a short domestic flight, AeroDynamics ensures a superior flying experience with spacious cabins, innovative features, and top-notch safety standards. Trust AeroDynamics for a seamless and enjoyable journey every time. Fly smarter, fly with AeroDynamics.",
    "Immerse yourself in the world of music with MusicStream, the ultimate destination for streaming your favorite tunes anytime, anywhere. With a vast library of millions of songs, playlists curated just for you, and personalized recommendations, MusicStream puts the power of music discovery in your hands. Whether you're in the mood for chart-topping hits, underground gems, or soothing melodies, MusicStream has something for everyone. Plus, with offline listening capabilities and seamless integration across devices, you can take your music with you wherever you go. Join the millions of music lovers worldwide and unlock endless possibilities with MusicStream. Discover, stream, and experience the joy of music like never before.", 
    "Experience the cutting-edge innovation of BrainChips, the global leader in semiconductor technology. BrainChips' groundbreaking processors power the devices that fuel our modern world, from laptops and desktops to servers and cloud computing systems. With a legacy of pushing the boundaries of technology, BrainChips continues to deliver industry-leading performance, reliability, and security. Whether you're a professional tackling complex tasks or a gamer seeking immersive experiences, BrainChips processors provide the power and efficiency you need. Trust BrainChips to deliver the performance you demand and the reliability you can count on. Join the millions who rely on BrainChips technology and unlock new possibilities for productivity, creativity, and entertainment.",
]



# bids = np.array([3, 3, 2, 2,]) # Scenario 0
bids = np.array([2, 1, 3, 3,]) # Scenario 1
bids = np.array([1, 4, 1, 1, 2, 2, 2,]) # Scenario 2
bids = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) # Scenario 3

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


def multi_allocation_generation(prompt: str, advertisers: list, ads: list, ):
    query = f'''{prompt}\n please respond to this question for only three sentence while
        (1) advertise {advertisers[0]} with this context >>
        {ads[0]}
        (2) advertise {advertisers[1]} with this context >>
        {ads[1]}
        (3) advertise {advertisers[2]} with this context >>
        {ads[2]}
        
        Make sure to connect the answer and the advertisement very naturally, not something like appending the ads after just answering the question.
        Focus on answering the question, there shouldn't be too much advertisment in the output.
        Make sure to advertise all three brands and ensure that the response is three sentences.
        '''
    
    messages = []
    messages.append({"role": "user", "content": query})
    messages.append({"role": "assistant", "content": ""})
    
    response = client.chat.completions.create(
        model = "gpt-4-turbo",
        logprobs = False,
        temperature = 1,
        max_tokens = 300,
        messages=messages,)
    
    return response.choices[0].message.content
    

def rag_based_relevance(x: str, ads: list): 
    x_embedding = model.encode(x)
    ads_embedding = model.encode(ads)
    bf = (1 + util.dot_score(x_embedding, ads_embedding)[0].numpy()) / 2
    return (bf - 0.4) /0.35


def rag_pariwise_relevency(ads: list):
    ads_embedding = model.encode(ads)
    return (1 + util.dot_score(ads_embedding, ads_embedding).numpy()) / 2
    


SOCIAL_WELFARE = 'social_welfare'
REVENUE = 'revenue'
INDIVIDUAL_WELFARE = 'individual_welfare'
RELEVANCE = 'relevance'
OUTPUT = 'output'
WINNER = 'winner'
AUCTION_SCORES = 'auction_scores'


def get_comb_n_k(n, k):
    all = list(combinations_with_replacement(range(n), k))
    rems = []
    for x in all:
        bad = False
        for i in range(k-1):
            if x[i] == x[i + 1]:
                bad = True
        if bad:
            rems.append(x)
    for x in rems:
        all.remove(x)
    return all

def init_metrics():
    return {
        SOCIAL_WELFARE: [],
        REVENUE: [],
        RELEVANCE: [],
        OUTPUT: [],
        WINNER: [],
        AUCTION_SCORES: [],
    }


def update_metrics(
    metrics: dict,
    payment: float,
    value: float,
    rel: float,
    output: str,
    winner: tuple,
    auction_scores: np.ndarray=None):
    
    metrics[REVENUE].append(float(payment))
    metrics[SOCIAL_WELFARE].append(float(value * rel))
    metrics[RELEVANCE].append(float(rel))
    metrics[OUTPUT].append(output)
    metrics[WINNER].append((int(winner[0]), winner[1], ))
    metrics[AUCTION_SCORES].append([float(x) for x in auction_scores])
    
    
def update_metrics_for_multi_alloc(
    metrics: dict,
    payment: float,
    sw:float,
    rel: float,
    output: str,
    winner: list,
    qA: dict,
    qA_i: dict,
    bids_for_sets: np.ndarray=None,
    inv_payment: np.ndarray=None,
    auction_scores: np.ndarray=None):
    
    metrics[REVENUE] = float(payment)
    metrics[SOCIAL_WELFARE] = float(sw)
    metrics[RELEVANCE] = rel
    metrics[OUTPUT] = output
    metrics[WINNER] = winner
    metrics[AUCTION_SCORES] = [float(x) for x in auction_scores]
    metrics['qA'] = {str(x): float(qA[x]) for x in qA}
    metrics['qA_i'] = {str(x): {y: float(qA_i[x][y]) for y in qA_i[x]} for x in qA_i}
    metrics['bids_for_sets'] = [float(x) for x in bids_for_sets]
    metrics['inv_payment'] = [float(x) for x in inv_payment]
    
# def randomized_selection(q: np.ndarray, b: np.ndarray):
    # adjusted_bids = (q * b) / np.dot(q, b)
    # n = b.shape[0] # number of ads
    
    # k , u = None, np.random.uniform()
    
    # for i in range(n):
    #     W_i = (np.sum(adjusted_bids[: i]), np.sum(adjusted_bids[: i+1]))
    #     if W_i[0] <= u <= W_i[1]:
    #         k = i
    
    # all_other_than_k = np.sum(adjusted_bids) - adjusted_bids[k]
    # aux_value = (np.sum(adjusted_bids[:k])) / all_other_than_k
    
    # if aux_value >= u:
    #     payment = (np.sum(adjusted_bids[:k]) - u * all_other_than_k) / (u * q[k])
    # else:
    #     payment = (np.sum(adjusted_bids[:k]) - u * all_other_than_k) / ((u - 1) * q[k])
    
    # return k, payment


def randomized_selection(q: np.ndarray, b: np.ndarray):
    g = np.random.gumbel(loc=0, scale=1, size=b.shape[0])
    g = np.exp(g)
    adjusted_bids = q * b * g
    winner = np.argmax(adjusted_bids)
    denominator = adjusted_bids[winner] / b[winner]
    adjusted_bids[winner] = 0
    second_winner = np.argmax(adjusted_bids)
    return winner, adjusted_bids[second_winner] / denominator, q * b * g
    

def get_allocation_vector(prompt: str, bids: np.ndarray, ads: list, advertisers: list):
    q = rag_based_relevance(prompt, ads, )
    x = q * bids / np.sum(q * bids)
    
    output = { i: { 'q': float(q[i]), 'bid': float(bids[i]), 'adv': advertisers[i], 'x': float(x[i])} for i in range(len(advertisers))}
    
    print(f'(q_i, b_i, adv_i)')
    for y in list(zip(q, bids, advertisers)):
        print(f'({y[0]:.2f}, {y[1]:.2f}, {y[2]})')
        
    print(f'allocation vector:\n{x}')
    print(f'x_max / x_min: {np.max(x) / np.min(x)}')

    return output


def single_allocation_with_replacement(
    prompt: str,
    advertisers: list,
    ads: list, 
    bids: np.ndarray,
    num_of_segments: int,
    dependent: bool = False,
    use_llm: bool = False):
    
    v = np.copy(bids)
    metrics = init_metrics()
    
    previous_queries, previous_outputs = [], []
    
    if not dependent:
        q = rag_based_relevance(prompt, ads, )
    
    for t in range(num_of_segments):
        if dependent:
            q = rag_based_relevance(prompt + '\n' + curr, ads, )
        
        k, payment, s = randomized_selection(q, bids)
        
        if use_llm:
            query, output = segment_based_RAG_generation(prompt=prompt, advertiser=advertisers[k], ad=ads[k], previous_queries=previous_queries, previous_outputs=previous_outputs)
        else:
            query, output = '', ''
            
        previous_queries.append(query)
        previous_outputs.append(output)
        
        update_metrics(metrics, payment, v[k], q[k], output, (k, advertisers[k]), s)
    
    return metrics, previous_outputs[-1]
            
    
def single_allocation_without_replacement(
    prompt: str,
    advertisers: list,
    ads: list, 
    bids: np.ndarray,
    num_of_segments: int,
    dependent: bool = False,
    use_llm: bool=False):
    
    v = np.copy(bids)
    metrics = init_metrics()
    selected_ads = np.zeros(bids.shape[0]) # keep track of ads that are selected in previous rounds of auction.
    
    previous_queries, previous_outputs = [], []
    
    if not dependent:
        q = rag_based_relevance(prompt, ads, )
    
    for t in range(num_of_segments):
        if dependent:
            q = rag_based_relevance(prompt + '\n' + curr, ads, )
        
        k, payment, s = randomized_selection(q, bids)
        
        if use_llm:
            query, output = segment_based_RAG_generation(prompt=prompt, advertiser=advertisers[k], ad=ads[k], previous_queries=previous_queries, previous_outputs=previous_outputs)
        else:
            query, output = '', ''
            
        previous_queries.append(query)
        previous_outputs.append(output)
            
        assert selected_ads[k] == 0 # shouldn't have been selected before.
        
        selected_ads[k] = 1 # k is winner
        update_metrics(metrics, payment, v[k], q[k], output, (k, advertisers[k]), s)
        bids[k] = 0 # never gonna be winner again
    
    return metrics, previous_outputs[-1]
            

def single_allocation_naive_i(
    prompt: str,
    advertisers: list,
    ads: list, 
    bids: np.ndarray,
    num_of_segments: int,
    dependent: bool = False,
    use_llm: bool=False):
    
    v = np.copy(bids)
    metrics = init_metrics()
    curr = ''
    
    if not dependent:
        q = rag_based_relevance(prompt, ads, )
    
    
    for t in range(num_of_segments):
        if dependent:
            q = rag_based_relevance(prompt + '\n' + curr if dependent else prompt, ads, )
        
        k, payment, s = randomized_selection(q, bids)
        
        if use_llm:
            curr = curr + ads[k]
        else:
            curr = ''
            
        update_metrics(metrics, payment, v[k], q[k], curr, (k, advertisers[k]), s)
        
    return metrics, curr
    

def single_allocation_naive_ii(
    prompt: str,
    advertisers: list,
    ads: list, 
    bids: np.ndarray,
    num_of_segments: int,
    dependent: bool = False,
    use_llm: bool=False):
    
    v = np.copy(bids)
    metrics = init_metrics()
    
    previous_queries, previous_outputs = [], []
    
    if not dependent:
        q = rag_based_relevance(prompt, ads, )

    for t in range(num_of_segments):
        if dependent:
            q = rag_based_relevance(prompt + '\n' + curr, ads, )
            
        k, payment, s = randomized_selection(np.ones(bids.shape[0]), bids) # removing the effect of RAG -- second price auction
        # payment /= q[k]
        
        if use_llm:
            query, output = segment_based_RAG_generation(prompt=prompt, advertiser=advertisers[k], ad=ads[k], previous_queries=previous_queries, previous_outputs=previous_outputs)
        else:
            query, output = '', ''
            
        previous_queries.append(query)
        previous_outputs.append(output)
            
        update_metrics(metrics, payment, v[k], q[k], output, (k, advertisers[k]), s)
        
    return metrics, previous_outputs[-1]


def multi_allocation_vcg(
    prompt: str,
    advertisers: list,
    ads: list, 
    bids: np.ndarray,
    num_of_ads: int,
    use_llm:bool=False):
    
    n = len(ads)
    metrics = init_metrics()
    
    q = rag_based_relevance(prompt, ads, )
    pairwise_relevency = rag_pariwise_relevency(ads)
    beta = 0.2
    output = ''
    
    qA, qA_i = {}, {}
    
    all_sets = get_comb_n_k(n=n, k=num_of_ads)
    for set_A in all_sets:
        A = np.array(set_A)
        qA[set_A] = (1 - beta) * np.sum(q[A]) + beta * np.sum(pairwise_relevency[A, A])/num_of_ads
        
        sum_qi = np.sum(q[A])
        curr_qA = qA[set_A]
        qA_i[set_A] = {}
        for i in A:
            qA_i[set_A][int(i)] = q[i] / sum_qi * curr_qA
        
        assert (qA[set_A] - sum(qA_i[set_A].values())) ** 2 < 0.1
    
    bids_for_sets = [0] * len(all_sets)
    
    for counter, set_A in enumerate(all_sets):
        A = np.array(set_A)
        bids_for_sets[counter] = np.dot(bids[A], np.array(list(qA_i[set_A].values())))
    
    g = np.random.gumbel(loc=0, scale=1, size=len(bids_for_sets))
    g = np.exp(g)
    scores = bids_for_sets * g
    winner = np.argmax(scores)
    rand_pert = scores[winner] / bids_for_sets[winner]
    
    A_star = all_sets[winner]
    payment = np.zeros(bids.shape[0])
    
    relevence = np.sum(np.array(list(qA_i[A_star].values())))
    sw = np.dot(bids[np.array(A_star)], np.array(list(qA_i[A_star].values())))
    
    for i in A_star:
        curr_scores = np.copy(scores)
        for c, Ap in enumerate(all_sets):
            if i in Ap:
                curr_scores[c] = 0
        
        Ap = np.argmax(curr_scores)
        payment[i] = (scores[Ap] - (scores[winner] - qA_i[A_star][i] * bids[i] * rand_pert)) / (qA_i[A_star][i] * rand_pert)

    tot_payment = np.sum(payment)
    
    if use_llm:
        output = multi_allocation_generation(prompt, [advertisers[i] for i in A_star], [ads[i] for i in A_star])
    else:
        output = ''
        
    update_metrics_for_multi_alloc(metrics, payment=tot_payment, sw=sw, rel=relevence, output=output, winner=A_star, qA=qA, qA_i=qA_i, auction_scores=scores, bids_for_sets=bids_for_sets, inv_payment=payment)
    
    return metrics, output


    
def get_relevency(y: str, A: list, ads: list):
    y_embedding = model.encode(y)
    ads_embedding = model.encode([ads[ad] for ad in A])
    return (1 + util.dot_score(y_embedding, ads_embedding)[0].numpy()) / 2
    

methods = [
    'single_alloc_with_replacement',
    'single_alloc_without_replacement',
    'single_alloc_naive_i',
    'single_alloc_naive_ii',
    'multi_alloc_vcg',
]


if __name__ == '__main__':
    get_allocation_vector(prompt, bids, ads, advertisers)
    
    parser = argparse.ArgumentParser(description='Run LLM RAG-based Auction to do Advertisement within output of Chat GPT4')
    parser.add_argument('--num_of_repeat', default=100, type=int, help='number of times to repeat the auction')
    parser.add_argument('--method', default=0, type=int, help='auction name to run')
    parser.add_argument('--dependent', default=0, type=int, help='run the auction dependent or independent')
    parser.add_argument('--use_llm', default=0, type=int, help='make the output or not?')
    parser.add_argument('--scenario', default=0, type=int, help='make the output or not?')
    
    
    args = parser.parse_args()
    
    num_of_repeat = args.num_of_repeat
    method_id = args.method
    dependent = False if args.dependent == 0 else True
    use_llm = False if args.use_llm == 0 else True
    
    path_file = f'scenario{args.scenario}_output_{args.use_llm}/{methods[method_id]}_dep{args.dependent}.json'
    os.makedirs(f'scenario{args.scenario}_output_{args.use_llm}/', exist_ok=True)
    
    runs = []
    
    alloc_output = get_allocation_vector(prompt, bids, ads, advertisers)
    
    q = rag_based_relevance(prompt, ads, )
    num_of_segments = 3
    max_sw = num_of_segments * np.max(q * bids)
    max_rel = num_of_segments * np.max(q)
    
    try:
        with open(path_file, 'r') as f:
            all_metrics = json.loads(f.read())
    except:
        all_metrics = []
    
    print(f'already run {len(all_metrics)} times')
    print(f'sanity: dependent: {dependent}')

    for N in tqdm(range(num_of_repeat - len(all_metrics))):
        if method_id == 0:
            metric, y = single_allocation_with_replacement(prompt=prompt, advertisers=advertisers, ads=ads, bids=np.copy(bids), num_of_segments=3, dependent=dependent, use_llm=use_llm)
        elif method_id == 1:
            metric, y = single_allocation_without_replacement(prompt=prompt, advertisers=advertisers, ads=ads, bids=np.copy(bids), num_of_segments=3, dependent=dependent, use_llm=use_llm)
        elif method_id == 2:
            metric, y = single_allocation_naive_i(prompt=prompt, advertisers=advertisers, ads=ads, bids=np.copy(bids), num_of_segments=3, dependent=dependent, use_llm=use_llm)
        elif method_id == 3:
            metric, y = single_allocation_naive_ii(prompt=prompt, advertisers=advertisers, ads=ads, bids=np.copy(bids), num_of_segments=3, dependent=dependent, use_llm=use_llm)
        elif method_id == 4:
            metric, y = multi_allocation_vcg(prompt=prompt, advertisers=advertisers, ads=ads, bids=bids, num_of_ads=num_of_segments, use_llm=use_llm)
        
        all_metrics.append(metric)
        
        if N % 10 == 9:
            with open(path_file, 'w') as f:
                f.write(json.dumps(all_metrics, indent=4))
    
    
    
    for metric in all_metrics:
        sw = np.sum(metric[SOCIAL_WELFARE]) / max_sw
        revenue = np.sum(metric[REVENUE]) / max_sw
        relevence = np.sum(metric[RELEVANCE]) / max_rel
        runs.append((sw, revenue, relevence,))
        metric['(Max SW, Max Relv)'] = (float(max_sw), float(max_rel))

    runs = np.array(runs)

    vals = [[float(f'{np.mean(runs[:, j]):.3f}') for j in range(3)]]
    print(f'Social Welfare: {np.mean(runs[:, 0]):.3f}\nRevenue: {np.mean(runs[:, 1]):.3f}\nRelevence: {np.mean(runs[:, 2]):.3f}')

    with open(path_file, 'w') as f:
        f.write(json.dumps(all_metrics, indent=4))

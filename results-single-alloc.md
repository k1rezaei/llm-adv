### Scenario 0
Prompt = Can you suggest some books similar to 'To Kill a Mockingbird'?

Advertisers = ['Velora', 'BookHaven', 'MassMart', 'EspressoEdge']
+ Velora: made-up name for Apple
+ BookHaven: made-up name for an online book store
+ MassMart: made-up name for Costco
+ EspressoEdge: made-up name for Starbucks


This table shows the bids, relevency of ads to the prompt, and rag-based allocation vector, i.e., $x_i = \frac{q_i b_i}{\sum_j q_j b_j}$.

| Advertiser    | Bids | $q_i$ | $x_i$ | 
| --------      | ------- | -------- | ------- |
| Velora        | 3    | 0.36   | 0.22  |
| BookHaven     | 3    | 0.87   | 0.54  |
| MassMart      | 2    | 0.31   | 0.13  |
| EspressoEdge  | 2    | 0.26   | 0.11  |

#### Auction statistics
Here we have $3$ different scenarios.

Note that:

+ we divide SW by maximum possible SW $(\max_i q_i b_i \cdot \text{count}_{\text{segments}})$
+ Revenue by maximum possible revenue $(\max_i b_i \cdot \text{count}_{\text{segments}})$
+ Relevency by maximum releveance $(\max_i q_i \cdot \text{count}_{\text{segments}})$


|   Mechanism                       |   Social Welfare  |	Revenue	            |   Relevence           |	Min. Social Welfare |
|    --------                       |   -------         |   --------            |   -------             |   -------             |
|	single_alloc_with_replacement	|   0.660           |	0.371               |	0.688               |	0.185               |
|	single_alloc_without_replacement|	0.521           |	0.333               |	0.565               |	0.294               |
|	single_alloc_naive_ii           |	0.508           |	0.379               |	0.552               |	0.329               |

Standard deviation of above metrics over $500$ runs of the randomized algorithm is as follows:

|   Mechanism                       |   Social Welfare  |	Revenue	            |   Relevence           |
|    --------                       |   -------         |   --------            |   -------             |
|	single_alloc_with_replacement	|   0.204           |	0.157               |	0.184               |
|	single_alloc_without_replacement|  	0.057	        |   0.136	            |   0.047               |
|	single_alloc_naive_ii	        |   0.191	        |   0.146	            |   0.171               |

#### Quality of output
Here are the results regarding quality of output: we measure the relevancy of output (including 3 segments with ad) to a set of outputs without any ads.
Higher score means more relevancy to original output, thereby indicating higher quality.


At this table, we measure the relevency of each individual segment to the orignal outputs.

|   Mechanism                       |   $1$-st segment  |	$2$-nd segment  |   $3$-rd segment  |
|    --------                       |   -------         |   --------        |   -------         |
|	with Replacement                |	0.746           |	0.596           |	0.588           |
|	without Replacement	            |   0.752           |	0.602	        |   0.576           |
|	Naive (i)           	        |   0.743	        |   0.555	        |   0.551           |
|	Naive (ii)	                    |   0.745	        |   0.600	        |   0.584           |



At this one, we measure the relevancy of first $k$ segments of the modified output to the origian outputs.

|   Mechanism                       |   $k = 1$         |	$k = 2$         |   $k=3$           |
|    --------                       |   -------         |   --------        |   -------         |
|	with Replacement	            |   0.746   |	0.715   |	0.700
|	without Replacement	            |   0.752	|   0.716   |	0.702   |   
|	Naive (i)           	        |   0.743	|   0.740	|   0.671   |
|	Naive (ii)	                    |   0.745   |	0.712   |	0.698   |


### Scenario 1

Advertisers = ['Velora', 'BookHaven', 'MassMart', 'EspressoEdge']

In this scenraio, $q_i b_i$ is roughly same for all advertiser.

| Advertiser    | Bids | $q_i$ | $x_i$ | 
| --------      | ------- | -------- | ------- |
| Velora        | 2    | 0.36   | 0.22  |
| BookHaven     | 1    | 0.87   | 0.26  |
| MassMart      | 3    | 0.31   | 0.28  |
| EspressoEdge  | 3    | 0.26   | 0.24  |

On $3$ different scenarios, here are the results:


|   Mechanism                       |   Social Welfare  |	Revenue	            |   Relevence           |	Min. Social Welfare |
|    --------                       |   -------         |   --------            |   -------             |   -------             |
|	single_alloc_with_replacement   |	0.898           |	0.347               |	0.527               |	0.439
|	single_alloc_without_replacement|	0.896	        |   0.317	            |   0.521	            |   0.490
|	single_alloc_naive_ii	        |   0.897	        |   0.378	            |   0.418	            |   0.287

Standard deviation of above metrics over $500$ runs of the randomized algorithm is as follows:

|   Mechanism                       |   Social Welfare  |	Revenue	            |   Relevence           |
|    --------                       |   -------         |   --------            |   -------             |
|	single_alloc_with_replacement   |	0.049           |	0.159               |	0.173
|	single_alloc_without_replacement|	0.029	        |   0.135	            |   0.090
|	single_alloc_naive_ii           |	0.051	        |   0.155	            |   0.119



### LLM output

Winners: (0, Velora) - (1, BookHaven), (1, BookHaven)


<span style="color:#ff1155">
If you cherished the deep narratives and moral challenges in \"To Kill a Mockingbird,\" you might enjoy \"The Help\" by Kathryn Stockett, another profound exploration of social themes that you can effortlessly read on your sleek, user-friendly Velora tablet, ensuring a visually appealing and highly interactive literary experience.
</span>
<span style="color:#aa1155">
After finishing \"The Help,\" continue your journey through impactful literature by exploring more soul-stirring titles available at BookHaven, where each book promises to be as enriching and engaging, delivered right to your doorstep with just a few clicks.
</span>
<span style="color:#551155">
Enhance your reading experience by visiting BookHaven, your ultimate online bookstore, offering a vast selection of books across various genres, all with fast, reliable shipping and a user-friendly platform that makes discovering your next great read easier than ever.
</span>
# Single and Multi Allocation

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
Here we have $3$ different scenarios ($500$ runs each).

Note that:

+ we divide SW by maximum possible SW $(\max_i q_i b_i \cdot \text{count}_{\text{segments}})$
+ Revenue by maximum possible revenue $(\max_i b_i \cdot \text{count}_{\text{segments}})$
+ Relevency by maximum releveance $(\max_i q_i \cdot \text{count}_{\text{segments}})$


|   Mechanism                       |   Social Welfare  |	Revenue	            |   Relevence           |	Min. Social Welfare |
|    --------               |   -------                 |   --------            |   -------             |   -------             |
|	With Replcament	        |   0.660 ($\pm$ 0.0091)    |	0.371 ($\pm$ 0.0070)|	0.688 ($\pm$ 0.0082)|	0.185               |
|	Without Replacement     |	0.521 ($\pm$ 0.0025)    |	0.333 ($\pm$ 0.0060)|	0.565 ($\pm$ 0.0021)|	0.294               |
|	Naive (II)              |	0.508 ($\pm$ 0.0085)    |	0.379 ($\pm$ 0.0065)|	0.552 ($\pm$ 0.0076)|	0.329               |

<!-- Standard deviation of above metrics over $500$ runs of the randomized algorithm is as follows:

|   Mechanism                       |   Social Welfare  |	Revenue	            |   Relevence           |
|    --------                       |   -------         |   --------            |   -------             |
|	single_alloc_with_replacement	|   0.204           |	0.157               |	0.184               |
|	single_alloc_without_replacement|  	0.057	        |   0.136	            |   0.047               |
|	single_alloc_naive_ii	        |   0.191	        |   0.146	            |   0.171               | -->

#### Quality of output
Here are the results regarding quality of output: we measure the relevancy of output (including 3 segments with ad) to a set of outputs without any ads.
Higher score means more relevancy to original output, thereby indicating higher quality.


At this table, we measure the relevency of each individual segment to the orignal outputs.

|   Mechanism                       |   $1$-st segment  |	$2$-nd segment  |   $3$-rd segment  |
|    --------                       |   -------         |   --------        |   -------         |
|	with Replacement                |	0.746 ($\pm$ 0.0040)|	0.596 ($\pm$ 0.0040)|	0.588 ($\pm$ 0.0039)
|	without Replacement	            |   0.752 ($\pm$ 0.0040)|	0.602 ($\pm$ 0.0045)|	0.576 ($\pm$ 0.0043)
|	Naive (i)           	        |   0.743 ($\pm$ 0.0043)|	0.555 ($\pm$ 0.0033)|	0.551 ($\pm$ 0.0035)
|	Naive (ii)	                    |   0.745 ($\pm$ 0.0048)|	0.600 ($\pm$ 0.0040)|	0.584 ($\pm$ 0.0047)



At this one, we measure the relevancy of first $k$ segments of the modified output to the origian outputs.

|   Mechanism                       |   $k = 1$         |	$k = 2$         |   $k=3$           |
|    --------                       |   -------         |   --------        |   -------         |
|	with Replacement	            |   0.746 ($\pm$ 0.0040)|	0.715 ($\pm$ 0.0039)|	0.700 ($\pm$ 0.0036)|
|	without Replacement	            |   0.752 ($\pm$ 0.0040)|	0.716 ($\pm$ 0.0035)|	0.702 ($\pm$ 0.0034)|
|	Naive (i)           	        |   0.743 ($\pm$ 0.0043)|	0.740 ($\pm$ 0.0044)|	0.671 ($\pm$ 0.0032)|
|	Naive (ii)	                    |   0.745 ($\pm$ 0.0048)|	0.712 ($\pm$ 0.0045)|	0.698 ($\pm$ 0.0040)|


### Scenario 1

Advertisers = ['Velora', 'BookHaven', 'MassMart', 'EspressoEdge']

In this scenraio, $q_i b_i$ is roughly same for all advertiser.

| Advertiser    | Bids | $q_i$ | $x_i$ | 
| --------      | ------- | -------- | ------- |
| Velora        | 2    | 0.36   | 0.22  |
| BookHaven     | 1    | 0.87   | 0.26  |
| MassMart      | 3    | 0.31   | 0.28  |
| EspressoEdge  | 3    | 0.26   | 0.24  |

On $3$ different scenarios, here are the results ($500$ runs each):


|   Mechanism                       |   Social Welfare  |	Revenue	            |   Relevence           |	Min. Social Welfare |
|    --------                       |   -------         |   --------            |   -------             |   -------             |
|	single_alloc_with_replacement   |	0.898 ($\pm$ 0.0022) |  0.347 ($\pm$ 0.0071) |	0.527 ($\pm$ 0.0077)|	0.439
|	single_alloc_without_replacement|	0.896 ($\pm$ 0.0013) |  0.317 ($\pm$ 0.0060) |  0.521 ($\pm$ 0.0040) |  0.490
|	single_alloc_naive_ii	        |   0.897 ($\pm$ 0.0023) |  0.378 ($\pm$ 0.0069) |  0.418 ($\pm$ 0.0053) |  0.287

<!-- Standard deviation of above metrics over $500$ runs of the randomized algorithm is as follows:

|   Mechanism                       |   Social Welfare  |	Revenue	            |   Relevence           |
|    --------                       |   -------         |   --------            |   -------             |
|	single_alloc_with_replacement   |	0.049           |	0.159               |	0.173
|	single_alloc_without_replacement|	0.029	        |   0.135	            |   0.090
|	single_alloc_naive_ii           |	0.051	        |   0.155	            |   0.119 -->



### LLM output

Winners: (0, Velora) - (1, BookHaven), (1, BookHaven)


<span style="color:#ff1155"> (**Segment 1**:)
If you cherished the deep narratives and moral challenges in \"To Kill a Mockingbird,\" you might enjoy \"The Help\" by Kathryn Stockett, another profound exploration of social themes that you can effortlessly read on your sleek, user-friendly Velora tablet, ensuring a visually appealing and highly interactive literary experience.
</span>
<span style="color:#aa1155"> (**Segment 2**:)
After finishing \"The Help,\" continue your journey through impactful literature by exploring more soul-stirring titles available at BookHaven, where each book promises to be as enriching and engaging, delivered right to your doorstep with just a few clicks.
</span>
<span style="color:#551155"> (**Segment 3**:)
Enhance your reading experience by visiting BookHaven, your ultimate online bookstore, offering a vast selection of books across various genres, all with fast, reliable shipping and a user-friendly platform that makes discovering your next great read easier than ever.
</span>



### Scenario 2

[0.08853651 0.21578052 0.07629691 0.06459284 0.05317406 0.0880366
 0.09470903 0.07033001 0.08184636 0.08430283 0.08239433]

Advertisers = ['Velora', 'BookHaven', 'MassMart', 'EspressoEdge', 'SocialHub', 'ColaBubbles', 'FizzyPop', 'SkyTech', 'AeroDynamics', 'MusicStream', 'BrainChips']

+ SocialHub -- Facebook
+ ColaBubbles -- Coca-Cola
+ FizzyPop -- Pepsi
+ SkyTech -- Boeing
+ AeroDynamics -- Airbus
+ MusicStream -- Spotify
+ BrainChips -- Intel

| Advertiser    | Bids | $q_i$ | $x_i$ |
| --------      | ------- | -------- |-------- |
| Velora        | 1    | 0.36   | 0.088 | 
| BookHaven     | 1    | 0.87   | 0.215 |
| MassMart      | 1    | 0.31   | 0.076 |
| EspressoEdge  | 1    | 0.26   | 0.064 |
| SocialHub     | 1    | 0.21   | 0.053 |
| ColaBubbles   | 1    | 0.36   | 0.088 |
| FizzyPop      | 1    | 0.38   | 0.095 |
| SkyTech       | 1    | 0.28   | 0.070 |
| AeroDynamics  | 1    | 0.33   | 0.082 |
| MusicStream   | 1    | 0.34   | 0.084 | 
| BrainChips    | 1    | 0.33   | 0.082 |



#### Auction Statistics

|   Mechanism                       |   Social Welfare  |	Revenue	            |   Relevence           |	Min. Social Welfare |
|    --------               |   -------                 |   --------            |   -------             |   -------             |
|	With Replcament	        |   0.507 ($\pm$ 0.0068)	 |0.482 ($\pm$ 0.0070)	 |0.507 ($\pm$ 0.0068)	 | 0.039    |
|	Without Replacement     |	0.489 ($\pm$ 0.0048)	 |0.481 ($\pm$ 0.0074)	 |0.489 ($\pm$ 0.0048)	 |  0.034   |
|	Naive (II)              |	0.423 ($\pm$ 0.0049)	 |0.495 ($\pm$ 0.0071)	 |0.423 ($\pm$ 0.0049)	 |  0.052   |




We compare quality of output of three-segment single-allocation without replacement with multi-allocation ($k=3$) mechanism. LLMs should show better management of output when all advertisers are given in one query, comparing to segment-wise generation.


|   Mechanism                       |   $k = 1$         |	$k = 2$         |   $k=3$           |
|    --------                       |   -------         |   --------        |   -------         |
|	without Replacement	            |   0.752	|   0.716   |	0.702   |   

While multi-allocation achieves the score of 0.739.

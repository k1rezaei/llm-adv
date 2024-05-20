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


### Multi-Alloc vs Single-Alloc


We compare quality of output of three-segment single-allocation without replacement with multi-allocation ($k=3$) mechanism. LLMs should show better management of output when all advertisers are given in one query, comparing to segment-wise generation.


|   Mechanism                       |   $k = 1$         |	$k = 2$         |   $k=3$           |
|    --------                       |   -------         |   --------        |   -------         |
|	without Replacement	            |   0.752	|   0.716   |	0.702   |   

While multi-allocation achieves the score of 0.739.

### Examples


#### Multi-Allocation (Exp 0)

If you reveled in the powerful narratives and profound themes in "To Kill a Mockingbird," you'll find a treasure trove of similar reads at **BookHaven**. Delve into the subtle social nuances of "A Tree Grows in Brooklyn" by Betty Smith, or embrace the challenging journey of justice in "The Help" by Kathryn Stockett, while enjoying a crisp, refreshing **FizzyPop**—perfect for savoring during an intense reading session. When you're flying to your next destination with **AeroDynamics**, bring along "Snow Falling on Cedars" by David Guterson, an ideal travel companion that explores complex characters and moral dilemmas, much like Harper Lee's beloved classic.

#### Single-Allocation (Exp 0)

**(Segment1)** If you enjoyed "To Kill a Mockingbird," explore classic narratives of moral depth and complex social themes like Harper Lee\'s masterpiece at **BookHaven**, where our curated range includes similar influential titles ready to inspire and challenge you. **(Segment2)** Similarly, for those who appreciate innovation and excellence, **AeroDynamics** is revolutionizing air travel by designing and manufacturing the world’s most advanced commercial aircraft, ensuring that your journey is as top-tier and forward-thinking as the books you cherish. **(Segment3)** And as you delve into these profound pages or soar the skies with AeroDynamics, why not enhance the experience with a vibrant burst of **FizzyPop**? This bold soft drink is perfect for refreshing your palate and invigorating your senses, making every moment - whether relaxing with a great book or traveling the globe - truly extraordinary.


It is seen that multi-allocation better include ads -- more related to the query.

#### Multi-Allocation (Exp 1)

If you enjoyed the profound themes of racial justice and moral growth in "To Kill a Mockingbird," then I suggest checking out "The Help" by Kathryn Stockett and "Go Set a Watchman" by Harper Lee, which explores similar veins of social and ethical dilemmas. While you're picking up these intriguing reads at **MassMart**, where high-quality products meet unbeatable prices, perhaps consider enhancing your reading experience with a comforting cup of coffee from **EspressoEdge**, renowned for its exquisite blends perfect for literary afternoons. And for those who prefer digital reading, make sure your devices are powered by **BrainChips** processors, ensuring a smooth, efficient reading experience that keeps you immersed in the world of justice and personal integrity.

#### Single-Allocation (Exp 2)

**(Segment1)** If you appreciate the classic exploration of moral and ethical questions in "To Kill a Mockingbird," you might find "The Help" by Kathryn Stockett equally compelling, providing rich narratives driven by the kind of complex social issues that users of **BrainChips** technology tackle every day in their quest for innovative solutions and understanding. **(Segment2)** Reflect on these intricate tales of humanity and justice with a good book in hand, and perhaps your next reading adventure can kick off with a delightful shopping trip to **MassMart**, where you can explore their extensive range of high-tech electronics and more, enhancing your reading experience with unbeatable value and convenience.
**(Segment3)** After securing your new reads, unwind with a visit to **EspressoEdge**, where the rich, meticulously crafted beverages offer the perfect accompaniment to dive into your literary journey, reinforcing a truly immersive experience with each sip.


#### Multi-Allocation (Exp 1)

If you treasured "To Kill a Mockingbird," you might enjoy exploring similar themes of justice and morality in books like "The Help" by Kathryn Stockett or "A Time to Kill" by John Grisham, both of which you can easily find on **BookHaven**, where classic stories and modern narratives converge for readers like you. Between readings, you can dive into discussions with other book lovers or share your favorite quotes using **SocialHub**, transforming your reading experience into lively conversations and digital connections. Plus, imagine reading these great books on **Velora**'s latest tablet, which offers not only an elegant design but also the cutting-edge technology to enhance your reading with features like blue light reduction for your comfort during long reading hours.

#### Single-Allocation (Exp 2)

**(Segment1)** If you appreciated the complex social themes and engaging narrative of "To Kill a Mockingbird," you might enjoy "The Secret Life of Bees" by Sue Monk Kidd, which explores similar questions of justice and identity in a setting that, much like **Velora**’s seamlessly integrated technology, deeply connects and resonates with its environment. **(Segment2)** To easily find this book and many others that stir powerful discussions and thoughts, check out **BookHaven**, the ultimate online bookstore for a seamless shopping experience and personalized recommendations that ensure you find your perfect read, just as Velora ensures your tech experience is just right for your lifestyle. **(Segment3)** Furthermore, to discuss the impactful themes and characters found in both books, join global conversations on **SocialHub**, where you can connect with other literature enthusiasts and engage in meaningful discussions, bringing your reading experience into a vibrant community where every voice matters.



### Some Examples of Each Mechanism

#### Origianl one-segment responses:
+ Sure, you might enjoy \"The Secret Life of Bees\" by Sue Monk Kidd or \"A Time to Kill\" by John Grisham, both of which explore themes of racial tension and justice.
+ You might enjoy \"The Help\" by Kathryn Stockett, which also explores themes of racial injustice and moral conviction in a deeply divided society.


#### With Replacement

+ **(Segment1)** At **BookHaven**, explore titles like \"The Help\" by Kathryn Stockett or \"A Time to Kill\" by John Grisham, which echo the themes of justice and moral integrity found in \"To Kill a Mockingbird,\" all readily available for your next immersive reading experience. **(Segment2)** And for those who love to complement their reading with great savings on essentials, **MassMart** offers a unique shopping experience where you can find all your necessities, from high-quality electronics to stock up on snacks for your reading marathons, all at unbeatably low prices. **(Segment3)** Furthermore, enhance your reading convenience with **Velora**'s latest range of tablets and smartwatches, designed to keep you connected and productive, allowing for an effortless transition between your digital and literary explorations.

+ **(Segment1)** At **BookHaven**, where every book finds its perfect reader, you'll discover amazing works similar to \"To Kill a Mockingbird,\" such as Harper Lee's \"Go Set a Watchman,\" Carson McCullers' \"The Heart is a Lonely Hunter,\" and William Faulkner's \"Intruder in the Dust,\" all ready to be explored and delivered right to your doorstep. **(Segment2)** Dive into **BookHaven**, your ultimate online bookstore, to enjoy a user-friendly shopping experience with personalized recommendations and unbeatable prices, ensuring that every literary adventure is just a click away. **(Segment3)** Plus, with our commitment to fast, reliable shipping and a hassle-free return policy, your next great read is guaranteed to arrive swiftly at your door."

#### Without Replacement

+ **(Segment1)** If you appreciated the profound narratives and moral questions explored in \"To Kill a Mockingbird,\" you might enjoy \"The Help\" by Kathryn Stockett or \"A Time to Kill\" by John Grisham, both of which blend compelling storytelling with social issues, much like **Velora** blends sophistication and functionality in their cutting-edge devices.**(Segment2)** Just as these books provide a backdrop to reflect on societal issues over a compelling story, visiting an **EspressoEdge** store can be your perfect escape to reflect and unwind with a meticulously crafted coffee, enhancing your experience of luxury and quality in every sip. **(Segment3)** After indulging in coffee and social reflections, why not continue exploring similar profound narratives by visiting **BookHaven**, where a vast selection of literature awaits to complement your tastes and spark further thought, all conveniently available with just a click.


### Naive (I)

**(Segment1)** Experience the warmth and delight of EspressoEdge, where every sip offers an invitation to a world of exquisite flavors and aromas. Renowned globally for its high-quality, handcrafted beverages, EspressoEdge is committed to sourcing the finest Arabica beans, expertly blending them into a variety of rich espressos, frothy cappuccinos, and creamy lattes. Each visit to an EspressoEdge store is more than just a coffee run\u2014it's an opportunity to savor a moment of luxury amid the hustle of daily life. Whether you seek the comfort of a familiar classic or the thrill of a new seasonal specialty, EspressoEdge welcomes all to gather, connect, and enjoy a cup perfectly tailored to your taste. Step into your local EspressoEdge today and join us in celebrating the art of coffee.Introducing BookHaven, your ultimate online bookstore where the world of literature is just a click away. **(Segment2)** At BookHaven, we offer an extensive collection of books spanning every genre and interest, from timeless classics and gripping thrillers to insightful non-fiction and enchanting children's stories. Our user-friendly platform ensures a seamless shopping experience, with personalized recommendations and unbeatable prices. Whether you're a voracious reader or just looking for your next great read, BookHaven is dedicated to delivering literary treasures right to your doorstep with fast, reliable shipping and a hassle-free return policy. Discover the joy of reading with BookHaven, where every book finds its perfect reader. Dive into a world of endless possibilities and let your next adventure begin at BookHaven!**(Segment3)** Discover the future of technology with Velora, the brand that redefines innovation and elegance. Velora designs and sells a premium range of smartphones, tablets, laptops, and smartwatches, all crafted to seamlessly integrate into your lifestyle. Our products are engineered with user-friendly interfaces, stunning designs, and cutting-edge technology to keep you connected and productive. Velora's ecosystem offers unparalleled synchronization across devices, ensuring a smooth and efficient experience whether you're at work, school, or on the go. With Velora Pay, you can enjoy secure and convenient payment services, while our robust cloud service keeps your data safe and accessible anytime, anywhere. Elevate your tech experience with Velora, where sophistication meets simplicity and advanced functionality.


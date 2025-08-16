---
title: "Turing tests in Chinese rooms: What does it mean for AI to outperform humans"
date: 2019-07-23
author: Dominik Lukeš
source: https://metaphorhacker.net/2019/07/turing-tests-in-chinese-rooms-what-does-it-mean-for-ai-to-outperform-humans
---

TLDR;
-----

* Reports that AI beat humans on certain benchmarks or very specialised tasks don’t mean that AI is actually better at those tasks than any individual human.
* They certainly don’t mean that AI is approaching the task with any of the same understanding of the world people do.
* People actually perform 100% on the tasks when administered individually under ideal conditions (no distraction, typical cognitive development, enough time, etc.) They will start making errors only if we give them too many tasks in too short a time.
* This means that just adding more of these results will NOT cumulatively approach general human cognition.
* But it may mean that AI can replace people on certain tasks that were previously mistakenly thought to require general human intelligence.
* All tests of artificial intelligence suffer from Goodart’s law.
* A test more closely resembling an internship or an apprenticeship than a gameshow may be a more effective version of the Imitation Game.
* Worries about ‘superintelligence’ are very likely to be irrelevant because they are based on an unproven notion of arbitrary scalability of intelligence and ignore limits on computability.

Reports of my intelligence have been greatly exaggerated
--------------------------------------------------------

Over the last few years, there have been various pronouncements about AI being better than humans at various tasks such as image recognition, speech transcription, or even translation. And that’s not even taking into account bogus winners of the Turing test challenge. To make things worse, there’s always the implication that this is means machine learning is getting closer to human learning and artificial intelligence is only a step away from going general.

All of those reports were false. Every. Single. One. How do we know this? Well, because none of them were followed by “and therefore we have decided to replace all humans doing job X with machine learning algorithms”. But even if this were the case, it still would not necessarily mean that the algorithm outperformers humans at the task. Just that it can outperform them at the task when it is repeated time after time and the algorithm ends up making fewer mistakes because, unlike people, it does not get tired, distracted, or simply ticks the wrong box.

But even if the aggregate number of errors is lower for a machine learning algorithm, it may still not make sense to use it because it makes qualitatively different errors. Errors that are more random and unpredictable are worse than more systematic errors that can be corrected for. Also, because AI has no metacognitive mechanisms to identify its errors by doing a ‘sense check’. This often makes correcting AI-generated transcripts difficult to correct because it makes errors that don’t make intuitive sense.

Pattern matching in radiology and law
-------------------------------------

The closest machine learning has gotten to outperforming humans doing real jobs is in radiology. (I’m discounting games like Go, here.) But even here it only equalled the performance of the best experts. However, this could easily be enough. But interpreting X-Rays is an extremely specialised task that requires lots of training and has a built-in error rate. It is a pattern recognition exercise, not a general reasoning exercise. All the general reasoning about the results of the X Rays still has to be delegated to the human physician.

In a similar instance, AI could notice inconsistencies in complex contracts better than lawyers. Again, this is very plausible, but again this was a pattern-matching exercise with a machine pitted against human distractability and stamina. Definitely impressive, useful, and not something expected even a few years ago. But not in any meaningful ways replacing the lawyer any more than a form to draw up a contract I downloaded from the internet does.

This is definitely a case where an AI can significantly augment what an unassisted human can do. And while it will not replace radiologists or lawyers as a category, it could certainly greatly decrease their numbers.

Machine learning to the test
----------------------------

So on very specialised tasks involving complex pattern recognition, we could say that AI can genuinely outperform humans.

But in all the instances involving language and reasoning tasks, even if an AI beats humans on a test, it does not actually ‘outperform’ them on the task. That’s because tests are always imperfect proxies for the competence they measure.

For example, native speakers often don’t get 100% on English proficiency tests and can even do worse than non-native speakers in certain contexts. Why? Three reasons: 1. They can imagine contexts not expected of non-native speakers. 2. The non-native speakers have been practicing taking these tests a lot so they make fewer formal mistakes.

We are facing exactly the same problems when comparing machine learning and human performance based on tests designed to evaluate machine learning. Humans are the native speakers and they perform 100% on all the tasks in their daily lives. But their performance seems less than perfect in test conditions.

### BLEU and overblown claims about Machine Translation

Sometimes the problem is with a poorly designed test. This is the case with the common measure of machine translation called [BLEU (Bi-Lingual Evaluation Understudy)](https://en.wikipedia.org/wiki/BLEU). BLEU essentially measures how many similar words or word pairs there are in the translation by machine when compared to a reference corpus of human translations. It is obvious that this is not a good metric of quality of translation. It can easily assign a lower score to a good translation and a high score to a patently bad one. For instance, it would not notice that the translation missed a ‘not’ and gave the opposite meaning.

What human translators do is translate whole texts NOT sentences. This sometimes means they drop things, add things, rearrange things. This involves a lot of judgment and therefore no two translations are ever the same. And outside trivial cases they’re never perfect. But a reliable translator can make sure they convey the key message and they could provide footnotes to explain where this was not possible. Machine learning can get surprisingly good at translating texts by brute force. But it is NOT reliable because it operates with no underlying understanding of the overall meaning of the text.

That’s why we can easily dismiss Microsoft’s claim that their English-to-Chinese interpreter outperformed human translators. That is only because they used the BLEU metric to make this claim rather than professional translators evaluating the quality of AI output against that of other professional translators on any test. And since Microsoft has yet to announce that it is no longer using human interpreters when its executives visit China, we can safely assume that this ‘outperform’ is not real.

Now, could a machine translation ever get good enough to replace human translators? Possibly. But it is still very far from that for texts of any complexity. Transformers are very promising at improving the quality of the translation but they still only match patterns. To translate you need to make quite rich inferences and we’re nowhere near this.

### GLUE and machine understanding come unstuck

Speaking of inferences. How good is AI at making those? Awful. Here we have another metric to look at: GLUE! Unlike BLEU which is a really bad representation of the quality of translation, [GLUE (General Language Understanding Evaluation)](https://gluebenchmark.com) is a really good representation of human intelligence. If you wanted to know what are the components of human intelligence, you could do a lot worse than look at the GLUE test.

But the [GLUE leaderboard](https:<span%20class="inline-comment">gluebenchmark.com/leaderboard) has a [human benchmark](https:</span>gluebenchmark.com/submission/xfBamAUrEBY0BWIVLx2uuGSmKvI2/-LXoXWPvqioRKAxCjt5W) and it comes 4th with 87.1% score. This puts it 1.4% behind the leader which is Facebook at 88.5%. So, it’s done. AI has not only reached human level of reasoning, it has surpassed them! Of course, not. Apart from the fact that we don’t know how much of a difference in reasoning ability 1% is, this tells us nothing about human ability to reason when compared to that of a machine learning model. Here’s why.

How people and machines make errors
-----------------------------------

I would argue that a successful machine learning algorithm does not actually outperform humans on these tasks even if it got 100%. Because humans also get 100% but they also devised the test.

Isn’t this a contradiction? How can humans get 100% if they consistently score in the mid-80s when given the test. Well, humans designed the test and the correctness criteria. And a machine learning algorithm must match the best human on every single answer to equal them. The benchmark here is just an average of many people over many answers and does not just reflect the human ability to reason but also the human ability to take tests.

Let’s explain by comparing what it means when a human makes an error on a test and when a machine does. There are three sources of human error: 1. Erroneous choice when knowing the right answer (ie clicking a when meaning to click b), 2. Lack of attention (ie choosing a because we didn’t spend enough time reading the task to choose correctly), 3. Overinterpretation (providing context in our head that makes the incorrect answer make sense).

These benchmarks are not Mensa tests, they measure what all people with typical linguistic and cognitive development can do. Let’s take the Windograd Schema test as an example. Here’s an often-quoted example:

> The **trophy** didn’t fit into the suitcase because **it**was too **big**.  
> The trophy didn’t fit into the **suitcase** because **it**was too **small**.

It is very possible that out of 100 people, 5 would get this wrong because they click the wrong answer, 10 because they didn’t process the sentence structure correctly and 1 because they constructed a scenario in their head in which it is normal for suitcases to be smaller than the thing in them (as in Terry Pratchett’s books).

But not a single one got it wrong because they thought that a thing can be bigger than the thing it fits in.

Now, when a machine learning model gets it wrong, it does it because it miscalculated a probability based on an opaque feature set it constructs from lots of examples. When you get 2 people together, they can always figure out the right answer and discuss why they did it wrong. No machine learning algorithm can do that.

This becomes even more obvious when we take an example from the actual GLUE benchmark:

> Maude and Dora had seen the trains rushing across the prairie, with long, rolling puffs of black smoke streaming back from the engine. Their roars and their wild, clear whistles could be heard from far away. Horses ran away when **they** came in sight.

So what does the ‘they’ refer to here? The obvious candidate here is ‘trains’. But it is easy to imagine that a person could click the option where ‘puffs of black smoke’ or even ‘Maude and Dora’ are the antecedent. That’s because both of those can be ‘seen’ and could theoretically cause horses to run away. If this is the 10th sentence I’m parsing in a go, I may easily shortcut the rather complex syntactic processing. I can even see someone choosing “whistles” even though they cannot “come in sight” but are a very strong candidate for causing horses to run away. But nobody would choose ‘horses’ unless they misclicked. A machine learning algorithm very easily could do this simply because ‘they’ and ‘horses’ match grammatically.

But all of this is actually irrelevant, because of how the ML algorithms are tested. They are given multiple pairs or sentences and asked to say 1 or 0 on whether they match or not. So some candidate sentences above are “Horses ran away when the trains came in sight.”, “Horses ran away when Maude and Dora came in sight.” or “Horses ran away when the whistles came in sight.” What it does NOT do is ask “Which of the words in the sentence does ‘they’ refer to?” Because the ML model has no understanding of such questions. You would have to train it for that task separately or just write a sequential algorithm to process these questions.

What people running these contests also cannot do is ask the model to explain their choice in a way that would show some understanding. There is a lot of work being done on interpretability, but this just spits out a bunch of parameters that have to be interpreted by people. Game, set and match to humans.

Chinese room revisited
----------------------

But let’s also think about what it means for a neural network model to get things right. This brings us back to Searl’s famous Chinese room argument. Every single choice a model makes has assigned a probability and even quite ridiculous choices have a non-zero chance of being right in the model. Let’s look at another common example:

> The animal didn’t cross the road because **it** was too busy.

Here it is sensible to assign **it** to ‘road’ because it makes the most sense but one could imagine a context in which we could make **it** refer to ‘the animal’. Animals can be thought of as busy and we can imagine that this could be a reason for not crossing the road. But we know with 100% certainty that **it** does not refer to ‘the’ or even ‘cross’. Yet, a neural model has no such assurance. It may never choose ‘the’ in practice as the antecedent for ‘it’ but it will never completely discount it, either.

So, even if the model got everything right. We could hardly think of it as making human-like inferences unless it could label certain antecedents as having 0% probability and others (much rarer) as having 100%. (Note: Programming it to change 10% to 0% or 90% to 100% does not count.)

This feels like a very practical expression of Searl’s [Chinese room argument](https://en.wikipedia.org/wiki/Chinese_room) albeit in a weak form. Neural networks pose a challenge to Searl because their algorithmic guts are not as exposed as those of the expert systems of Searl’s time. But we can still see echoes of their lack of actual human-like reasoning in their scores.

Is a test of artificial intelligence possible under Goodhart’s Law?
-------------------------------------------------------------------

> I once attended a conference on AI risk where a skeptic said he wasn’t going to worry “until an AI could do Winograd schemas”. This referred to a test of common sense and linguistic ambiguity that AIs have long been famously bad at. Now[Microsoft claims](https:<span%20class="inline-comment">blogs.msdn.microsoft.com/stevengu/2019/06/20/microsoft-achieves-human-performance-estimate-on-glue-benchmark) to have developed a new AI that is comparable to humans on this measure. ([Scott Alexander](https:</span>slatestarcodex.com/2019/06/26/links-6-19))

This post was inspired by the above remark by Scott Alexander. I wanted to explain why even the Winograd challenge being conquered is not enough in and of itself.

AI proponents constantly complain of sceptics’ shifting standards. When AI achieves a benchmark, everybody scrambles to find something else that could be required of it before it gets a pass. And I admit that I may have made a claim similar to that of the AI researcher quoted by Scott Alexander when I was writing about the Winograd schemas.

But the problem here is not that machines became intelligent and everybody is scrambling to deny the reality. The problem is that they got better at passing the test in ways that nobody envisioned when the test was designed. All this while taking no steps towards actual intelligence. Although with a possible increase in practical utility.

This is the essence of Goodhart’s Law: “When a measure becomes a target, it ceases to be a good measure.” The Winograd Schema Challenge seemed so perfect. Yet, I can imagine a machine learning getting good at passing the challenge but still not actually having any of the cognition necessary to really deal with the tasks in real life. In the same way that IBM Watson got really good at Jeopardy but failed at everything else.

None of this is to say that machine learning could not get good enough at performing many tasks that were previously thought to require generalised cognitive capacity. But when machines actually achieve human-level artificial intelligence, we will know. It will not be that hard to tell. But it will not likely happen just because we’re doing more of the same.

The problem with the Turing test or imitation game is not that it cannot produce reliable results on any one run of it. The problem is that if any single test becomes not only the measure but also a target, it is very much possible to focus on passing the test on the surface while bypassing the underlying abilities the test is meant to measure. But the problem is not just with the individual tests but rather in the illusion that we can design a test that will determine AGI level performance simply by reaching an arbitrary threshold.

The current Turing test winners won by misdirection that hid the fact that they refused to answer the questions. This could be fixed by requiring that [Grice’s cooperative principle maxims](https://en.wikipedia.org/wiki/Cooperative_principle#Grice's_Maxims) are observed (especially quality and relevance) but even then, I could see a system trained to deal with a single time-bound conversation pass without any underlying intelligence.

As [Scott Aaronson showed](https://www.scottaaronson.com/blog/?p=1858), it is possible to defeat a current level AI system simply by asking ‘What is bigger a shoebox or Mount Everest’. But once a pattern of questioning becomes known, it becomes a target and therefore a bad measure.

Similar things happen with all standardised aptitude tests designed so that they cannot be studied for. Job interview techniques designed to get interviewees to reveal their inner strengths and weaknesses. All of these immediately spawn industries of prep schools, instructional guides, etc. That makes them less useful over time (assuming they were all that useful to start with).

Towards a test by Critical Turing Internship
--------------------------------------------

That’s why the Turing test cannot be a ‘test’ in the traditional sense. At the very least, it cannot be a single test.

History and a lot of human-computer interaction research has also shown that people are very bad at administering the Turing test (or playing the imitation game). But this is paradoxically because they’re very good the very thing the machines have been failing at: meaning making. Because we almost never encounter meaningless symbols but often encounter incomplete ones, we are conditioned to always infer some sort of meaning from any communication. And it is difficult if not impossible to turn it off.

Every time we see a bit of language we automatically imbue it with some meaning. So, any Turing tester must not only be trained in the principles of cognition but also to discard their own linguistic instincts. We don’t know what it will take for a machine to become truly intelligent but we do know that humans are notoriously bad at telling machines apart from other humans. We simply cannot entrust this sort of thing to such feeble foundations.

As I said above, I suspect that by the time machines do achieve human-level performance on these tasks, it will be obvious. We probably won’t need such a test. Assuming we get there which is not a given. But if a test were needed, it could look something like this.

To replace the Turing test, I would like to propose a sort of Turing Internship. We don’t entrust critical tasks in fields like medicine to people who just passed a test but require they prove ourselves in a closely supervised context. In the same way, we should not trust any AI system based on a benchmark.

Any proposed human-level AI system can be placed in multiple real contexts with several well-informed human supervisors who would monitor its performance for a period of weeks or months to allow for any tricks to be exposed. For example, most people after a few weeks with Alexa, Google Assistant or Siri, get a clear picture of its strengths and limitations. Five minutes with Alexa may make you feel like the singularity is here. Five months will firmly convince you that it is nowhere in sight.

But at the moment, we don’t need this. We don’t need months or weeks to evaluate AI for human-level intelligence. We need minutes. I estimate that we would not need to use this kind of AI internship for another 50 years but likely for much much longer. We are too obssessed with the rapid progress of some basic technologies but ignore many examples of stagnation. My favourite here is the Roomba which has been on the market for 17 years now and has hardly progressed at all. Equally, the current NLP technologies have made massive strides in utility but have not progressed towards anything that could be meaningfully described as understanding.

That is not to say that tests like GLUE or even BLUE are completely useless. They can certainly help us compare ML approaches (up to a point). They’re just useless for comparing human performance with those of machine-generated models.

Note on Nick Bostrom and Superintelligence
------------------------------------------

One obvious objection to the Turing Internship idea is that if human-level AI is the last step before Bostrom’s ‘Superintelligence’, unleashing it in any real context would be extremely dangerous.

If you believe in this ‘demon in the machine’ option, there’s nothing I can do to convince you. But I personally don’t find Superintelligence in any way persuasive. The reason is that most of the scenarios described are computationally infeasible in the first place. Bostrom does not mention the issue of computability and things like P=NP almost at all. And he completely ignores questions of nonlinear complexity.

It is hard to judge whether a ‘superintelligent’ system could take over the world. But could it predict the weather 20 days out with 1% tolerance of temperature estimates in any location? The answer is most likely not. There may not be enough atoms in the universe to compute the weather arbitrarily precisely more than a few days in advance. Could it predict earthquakes? Could it run an economy more efficiently than an open market relying on price signals? The answers to all those questions are most likely no. Not because the superintelligence is not super enough but because these may not be problems that can be solved by adding ‘more’ intelligence. Assuming that ‘intelligence’ is a linearly scalable property in the first place. It may well be like body size, after a certain amount of increase, it would just collapse onto itself.

Superintelligence requires a conspiracy theorist’s mindset. Not that people who believe are conspiracy theorists. But they assume that complexity can be conquered with intelligence. They don’t believe that humans are ‘smart’ enough to control everything. But they believe that it is inherently possible. Everything we know about complexity, suggests that this is not the case. And that is why I’m not worried.

### *Related*
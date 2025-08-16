---
title: "Does machine learning produce mental representations?"
date: 2018-05-28
author: Dominik Lukeš
source: https://metaphorhacker.net/2018/05/does-machine-learning-produce-mental-representations
---

TL;DR
-----

* Why is this important? Many people believe that mental representations are the next goal for ML and a prerequisite for AGI.
* Does machine learning produce mental representations equivalent to human ones in kind (if not in quality or quantity)? Definitely not, and there is no clear pathway from current approaches to a place where it would. But it is worth noting that mental representations in humans are also not something straightforward to identify or describe.
* Is there a currently viable approach to ML that could eventually lead to mental representations with more engineering? It appears not but then again, no one expected neural nets would get so successful.

**Update:** Further **[discussion on Reddit](http://metaphorhacker.net/2018/05/does-machine-learning-produce-mental-representations/)****.**

Background
----------

Over the last few months, I’ve been catching up more systematically on what’s been happening in machine learning and AI research in the last 5 years or so and noticed that a lot of people are starting to talk about the neural net developing a ‘mental’ representation of the problem at hand. As someone who’s preoccupied with mental representations a lot, this struck me as odd because what was being described for the machine learning algorithms did not seem to match what else we know about mental representations.

So I’ve been formulating this post when I was pointed to this interview with [Judea Pearl](https://www.quantamagazine.org/to-build-truly-intelligent-machines-teach-them-cause-and-effect-20180515). And he makes exactly the same point:

“That sounds like sacrilege, to say that all the impressive achievements of deep learning amount to just fitting a curve to data. From the point of view of the mathematical hierarchy, no matter how skillfully you manipulate the data and what you read into the data when you manipulate it, it’s still a curve-fitting exercise, albeit complex and nontrivial.”

He continues:

“If a machine does not have a model of reality, you cannot expect the machine to behave intelligently in that reality.”

What does this model of reality look like? Pearl seems to reduce it to ‘cause and effect’ but I would suggest that the model needs more than that (Note: I haven’t read his book just the interview and [this intro](https://www.basicbooks.com/titles/judea-pearl/the-book-of-why/9780465097609/#module-whats-inside).)

What are mental representations?
--------------------------------

Mental representations are all sorts of images (ranging from rich to schematic and from static to dynamic) in our mind on which we draw sometimes consciously but mostly unconsciously to deal with the world. They are essential for producing and understanding language (from even the simplest sentence) and for basic reasoning. They can be represented as schemas, rich images, scenarios, scripts, dictionaries or encyclopedic entries. They can be in many modalities – speech, sound, image, moving picture.

Here are some examples to illustrate.

#### Static schemas

What does ‘it’ refer to in pairs of sentences such as these (example from [here](http://dataskeptic.com/blog/episodes/2018/winograd-schema-challenge)):

1. The *trophy* wouldn’t fit into the *suitcase* because **it** was too *big*.
2. The *trophy* wouldn’t fit into the *suitcase* because **it** was too *small*.

It takes no effort at all for a human to determine that **it** in (1) refers to *trophy* and in (2) to *suitcase*. Why, because, we have schemas of containment and we know almost intuitively that big things don’t fit into smaller things. And when we project that schema onto trophy and suitcase we immediately know what has to be too big or too small in order for one not to fit into the other.

You can even do it with a single sentence as in *Jane is standing behind Clare so you cannot see* ***her****.* It is clear that **her** refers to Jane and not Clare but only because we can project a schema of 2 similar-sized objects positioned relative to the observer’s line of sight.

So we also know that only sentence 1 below makes sense because of the schema we have for things of unequal size being positioned relative to each other and their impact on our ability to see them.

1. The statue is in front of the cathedral.
2. The cathedral is in front of the statue.

However, unlike with the trophy and suitcase, it is possible to imagine contexts in which sentence 2 would be acceptable. For instance, in a board game where all objects are printed on blocks of the same size and positioned on a 2D space.

This is to illustrate that the schemas are not static but interact with the rich conceptualisations we create in context.

#### Force dynamics

This is a notion pioneered by Leonard Talmy that explains many aspects of cognitive and linguistic processes through dynamic schemas of proportional interaction. Thus we know that all things being equal, bigger things will influence smaller things, faster things will overtake slower things, etc.

So we can immediately interpret the **it** in sentences such as:

1. The foot hit the ball and **it** flew off.
2. The bird landed on the perch and **it** fell apart.

But we also apply these to more abstract domains. We can thus easily interpret the situations behind these 2 sentences:

1. The mother walked in and the baby calmed down.
2. The baby walked in and the mother calmed down.

If asked to tell the story that led to 1 or 2, people would converge on very similar scenarios around each sentence.

#### Knowledge of the world

Sometimes, we marshall quite rich (encyclopedic) knowledge of the world in the process of constructing an understanding of what we hear or see. Imagine what is required to match the following 2 pairs of sentences (drawing on Langacker):

1. The Normans conquered England with …
2. The Smiths conquered England with….
3. a. … their moody music.
4. b. … their superior army.

Obviously the right pairings are 1b and 2a. But none of this is contained in the surface form. We must have the ‘encyclopedic’ knowledge of who The Normans and The Smiths were but also the force dynamic schemas of who can conquer who.

So on hearing the sentence ‘Mr and Mrs Smith conquered Britain’, we would be looking for some metaphorical mapping to explain the mismatch between the force we know conquering requires and the force we know a married couple can exert. With sufficiently rich knowledge, this is immediately obvious as in ‘John and Yoko conquered America.’

#### How does machine learning do on interpreting human mental representations?

For AI, examples such as the above are a difficult challenge. It was recently proposed that a much more effective and objective Turing test would be to ask an AI to interepret sentences such as these under the [ Winograd Schema Challenge] (<https://en.wikipedia.org/wiki/Winograd_Schema_Challenge)>.

A database of pairs of sentences such as:

1. The city **councilmen** refused the demonstrators a permit because **they** *feared* violence.
2. The city councilmen refused the **demonstrators** a permit because **they** *advocated* violence.

This has the great advantage of perfect objectivity. Unlike with the Turing test, it is always clear which answer is correct.

The best machine learning algorithms use various tricks but they still only do slightly better than chance (57%) at interpreting these schemas.

The only problem is that it is quite hard to construct these pairs in a way that could not be solved with simple statistical distributions. For instance, the Smiths and Normans example above could be easily resolved with current techniques simply by searching which words occur most frequently together.

Also, it is not clear how the schematic and force dynamic aspects interact with the encyclopedic aspects. Can you have one without the other? Can we classify the Winograd schema sentences into different types, some of which would be more suspectible to ML approaches?

### Do mental representations exist?

There is a [school of thought](http://psychsciencenotes.blogspot.co.uk) that claims that mental representations do not actually exist. There is nothing like what I described above in the brain. It is actually just a result of perceptual task orientation. This is the ecological approach developed in the study of perception and physical manipulation (such as throwing or catching a ball).

I am always very sceptical of any approach that requires we find some bits of information resembling what we see stored in the brain. Which is why I am quite sympathetic to the notion that there are no actual mental representations directly encoded into the synaptic activations of our brain.

But even if all of these were just surface representations of completely different neural processes, it is undeniable that something like mental representations is necessary to explain how we think at speak at some level. At the very least to articulate the problems that have to be solved by machine learning.

**Note:** I have completely ignored the problem of embodiment which would make things even more complicated. Our bodily experience of the world is definitely involved. But to what extent are our bodies actually a part of the reasoning process (as opposed to the brain as an independent computational contrl module) is a subject of hot debate.

How does machine learning represent the problem space?
------------------------------------------------------

Now, ML experts are not completely wrong to speak about representations. Neural nets certainly build some sort of representation of the problem space (note, I don’t call it world). We have 4 sources of evidence:

1. Structure of data inputs: Everything is a vector encoded as a string of numbers.
2. Patterns of activation in the neural nets (weights): This is where the ‘curve fitting’ happens.
3. Performance on real world tasks: More reliable than humans on dog breed recognition but penguins can also be identified as pandas.
4. Adversarial attacks: Adding seemingly random and imperceptible noise to a image or sound can make it produce radically different outputs.

If we take together the vector inputs and the weights on the nodes in the neural net, we have one level of representation. But that is perhaps the less interesting and as complexity increases, it becomes impossible to truly figure out much about it.

But is it possible that all of that actually creates some intermediate layer that has the same representational properties as mental representations? I would argue that at this stage, it is all inputs and weights and all the representational aspects are provided by the human interpreting the outputs. But if we only had the outputs, we could still posit some representational aspects. But the adversarial attacks reveal that the representational level is missing.

**Note:** Humans can also be subject to adversarial attacks with all sorts of perceptual and cognitive illusions. They seem to be on a different representational level to me but they would be worth exploring further in this context.

**Update:** A [commenter on Reddit](https://www.reddit.com/r/MachineLearning/comments/8moils/d_does_or_can_machine_learning_produce_mental/dzyauwj/) suggested that I look at this post on [feature visualisation](https://distill.pub/2017/feature-visualization/) and I think that mostly supports my point. It looks like there are lots of representations shown in that article, but they are really just visualisations of what inputs lead to certain neuron activations on specific layers of the neural net. Those are not ‘representations’ the neural net has independent access to. I think in the same way, we would not think of Pavlov’s dogs salivating on the sounds of the bell as having ‘mental representation’ of the ‘bell means food’ causal connection. Perhaps we could rephrase the question of whether training a neural net is similar to [classical or operant conditioning](https://en.wikipedia.org/wiki/Operant_conditioning). and what that means with respect to the question of representation.

Can we create mental representations in machines?
-------------------------------------------------

Judea Pearl thinks that nothing current ML is doing is going to lead to a ‘model of the world’ or as I call it ‘mental representations’. But I’m skeptical that his solution is a path to mental representations either:

“The first step, one that will take place in maybe 10 years, is that conceptual models of reality will be programmed by humans.”

This is what the early AI expert systems tried to do but it proved very elusive. One example of manually coding mental representations is [FrameNet](https://%3cspan%20class=%22inline-comment%22%3eframenet.icsi.berkeley.edu), a database of words linked to semantic frames but it barely scratches the surface. For instance, here’s the [frame for container](https://%3c/span%3eframenet2.icsi.berkeley.edu/fnReports/data/frameIndex.xml?frame=Containers) which links to suitcase. But that still doesn’t help with the idea of trophy being sometimes small enough to fit and sometimes too big. I can see how FrameNet could be used on very small subsets of problems but I don’t see a way for scaling it up in a way that could take into account everything involved in the examples I mentioned. We are faced with the curse of dimensionality here. The possible combinations just grow too fast for us to compute them.

I’m also not sure that simply running more data through bigger and bigger RNNs or CNNs will get us there either. But I can’t rule out that brute force won’t get us close enough for it not to matter that mental representations are not involved.

Perhaps, if label enough text of some subdomain with framenet schemas, we could train a neural net on this. But that will help with the examples where rich knowledge of the world is not required. We can combine a schema of a suitcase and a trophy with that of ‘fit’ and match ‘it’ with the more likely antecedent. Would that approach help with the demonstrators and councilmen? But even if so, the Winograd Schema Challenge is only an artificially constructed set of sentence pairs designed for a particular purpose. The mental representations involved crop up everywhere all the time. So we not only need a way of invoking mental representations but also a way to decide if they are needed and, if so, which ones.

Machine learning fast and slow up the garden path
-------------------------------------------------

Let’s imagine that we can somehow engineer a solution that can beat the Winograd Schema Challenge. Would that mean that it has created mental representations? We may want to reach for Searl’s [‘Chinese Room Argument’](https://plato.stanford.edu/entries/chinese-room) and the various responses to it. But I don’t think we need to go that deep.

One big aspect of human intelligence that is often lumped together with the rest is *metacognition*. This is the ability to bring the process of thinking (or speaking) to conscious awarenes and control it (at least to a degree). This is reminiscent of Kahneman’s two systems in ‘Thinking Fast and Slow’.

Machine learning produces almost exclusively ‘fast thinking’ – instantaneous matching of inputs to outputs. It is the great advance over previous expert system models of AI which tried to reproduce slow thinking.

Take for instance the famous [Garden path sentences](https://en.wikipedia.org/wiki/Garden_path_sentence). Compare these 2:

1. The horse raced past the barn quickly.
2. The horse raced past the barn fell.

Imagine the mental effort required to pause and retrace your steps when you reach the word ‘fell’ in the second sentence. It is a combination of instantanous production of mental images that crash and slow deliberate parsing of the sentence to construct a new image that is consistent with our knowledge of the world and the syntactic schema used to generate it.

Up until the advent of stochastic approaches to machine learning in the 1990s (and neural nets in 2010s), most AI systems tried to reproduce the slow thinking through expert systems encoded as decision trees. But they mostly failed because the slow thinking only works because of the fast thinking which provides the inputs to it. Now neural nets can match complex patterns that we once thought impossible. But they do it very differently from us. There doesn’t seem to be much thinking about how to go about developing the sort of metacognition that is required to combine the two. All of the conditional decisionmaking around what to do with the outputs of ML algorithms has to be hardcoded. Alexa can recognize my saying ‘turn on bedroom light’ but I had to give it a name and if I want to make it part of a more complex process (make sure bedroom light is off when I leave home), I have to go to IFTTT.

I don’t see how [Pearl’s approach](https://www.basicbooks.com/titles/judea-pearl/the-book-of-why/9780465097609/#module-whats-inside) will take us there. But I don’t see an alternative, either. Perhaps, the mental representations will emerge epiphenomenally as the neural nets grow and receive more sophisticated inputs about the spatial nature of world (rather than converting everything to vectors). Maybe they will be able to generate their own schemas as training inputs. I doubt it, but wouldn’t want to bet against it.

What is just as likely is that we will reach a plateau (maybe even resulting in a new [AI winter](https://en.wikipedia.org/wiki/AI_winter)) that will only see incremental improvements and won’t take the next step until a completely new paradigm emerges (which may not happen for decades if ever).

Conclusion
----------

It is not always obvious that more in-depth knowledge of a domain contributes to a better model of it. We are just as likely to overfit our models as to improve them when we dive too deep. But I think that mental representations at least reveal an important problem domain which should be somehow reflected in what machines are being taught to learn.

**Update**
----------

In response [to a comment on Reddit](https://www.reddit.com/r/MachineLearning/comments/8moils/d_does_or_can_machine_learning_produce_mental/dzyauwj/), I wanted to add the following qualification.

I think I ended up sounding a bit more certain than I feel. I know I’m being speculative but I note that all the critics are pointing at hypotheticals and picking at my definition of mental representation (which is not necessarily unwarranted).

But what I would like to hear is a description of the next 5 specific problems to be solved to get nearer to say 75% on the Winograd Schema Challenge that can then be built on further (ie not just hacking around collocation patterns Watson style).

I also wanted to note that I omitted a whole section on the importance of collocability in language with a reference to [Michael Hoey’s work on Lexical Priming](https://academic.oup.com/ijl/article-abstract/19/3/327/954608?redirectedFrom=fulltext), which I think is one of the 2 most important contributions to the study of language in the last 20 years, the other being William Crofts [Radical Construction Grammar.](https://books.google.co.uk/books/about/Radical_Construction_Grammar.html?id=3OwDr0gb9CcC&redir_esc=y) The reading of which would be of benefit to many ML researchers along with Fauconnier’s and Turner’s [The Way We Think](http://markturner.org/wwt.html).

### *Related*
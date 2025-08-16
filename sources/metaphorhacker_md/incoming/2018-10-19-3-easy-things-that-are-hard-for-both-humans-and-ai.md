---
title: "3 “easy” things that are hard for both humans and AI"
date: 2018-10-19
author: Dominik Lukeš
source: https://metaphorhacker.net/2018/10/3-easy-things-that-are-hard-for-both-humans-and-ai
---

Everybody is agog at what AI systems can do. Nobody thought even 10 years ago that machines could be trained to recognise images or transcribe natural speech as well as they do now. And because of this leap forward everybody has started worrying about AI taking over the world because it will soon be able to do everything people can but better.

On the other hand, there are AI naysayers who point at incredible feats of human creativity and ingenuity and say ‘no machines will ever be able to write a poem’ or ‘manage a company’.

While I’m more than skeptical about the true possibilities of AI, I am equally ekeptical about this supposed limitless human creativity that is beyond the bounds of computation.

I think we can reveal more about the limits and nature of human intelligence and thus the targets (possible limits) for AI development, if we look at very simple things with which both humans and AI struggle albeit in different ways.

Machines are often thought of as capable only of algorithmic processing (such as adding lots of numbers) and humans are thought to excel at massively parallel tasks – also known as intuition (such as telling part dogs from cats). But we will see that they seem to trade these roles in the ways they approach and fail at these appartently simple problems.

I call these problems ‘easy’ because they can be broken into very easy and straightforward components. But they are hard if not impossible in reality because of the curse of dimensionality. Even the slightest variation in those simple components, will grow into an exponential mess.

1. Figuring out time zones
--------------------------

Apple Watches recently stopped working because of Summer Time in Australia. And just the other day, Outlook asked me if I wanted to switch to a continental time zone in Europe. After I said yes, it started scheduling all meetings 2 hours off.

On the other hand, I’ve been arranging meetings between 2 time zones 1 hour apart for 20 years and I still get it wrong about 3 times out of 10.

So what gives? Time zones are conceptually very straightforward. You just have a database of times and places with notes on what time it is when and where relative to some fixed point. Then all you do is subtract anywhere between 1 and 12. What could be easier?

Well, you have to add in change of dates, so you have to switch between today, tomorrow and yesterday quite a lot. But still. There is a finite number of times and places and their combinations, so how hard can it be for human programmers to sit down and write all the code once and for all? Turns out, incredibly hard. There are just too many permutations and they keep changing as the database of times and places is being updated with new information.

So, the magnitude of the problem seems to be too great for humans to come up with exhastively detailed algorithms to deal with it. (To be clear, the core has been solved, but we don’t seem to be able to nail all the edge cases. Things would be a lot worse without computers.)

So why don’t we unleashe machine deep learning on the problem? Well, partly because there’s no good data for a machine to learn on. This is mostly an algorithmic problem. But the inputs of the algorithm come from very human perceptions of how time relates to cyclical things like days and relationships like comparing states between time zones with respect to days. Again, none of this is all that complex. But the algorithmic part is too complex for humans to describe as a series of if-then commands to a computer without making lots of mistakes. And the perspective and context part seems to be completely outside of what any ML algorithm can access at the moment.

So we’re stuck with something that mostly works but not always and is mostly understood but also always confusing.

2. Scheduling a meeting
-----------------------

Scheduling meetings is another simple algorithmic problem related to time. Simply compare two series of numbers, find where they differ and spit out the result. But all of this starts interacting with a lot of human complexities that make the problem completely intractable if what we wanted to do is write a series of commands in the form of ‘if you see this, do that’.

That’s why the work of the human assistant handling the scheduling for a busy person (who rates an assistant) is not just to provide her intelligence or understanding of calendars. It involves conversations with the person whose calendar is being managed about their priorities, options, possible scenarios, conversations with other people, other assistants, eventually arriving at some compromise which is then entered into the straightforward if-then format of a calendar.

It is this conversation with other people that is often overlooked (“tell your people to call my people”). In the case of the assistants of the other busy people who rate an assistant also have to synthesize the priorities and value of their charges through the same process of conversations and adjustments.

The final matching algorithm is very simple – so simple that it seems like noone should need a human assistant any more. But the inputs into the algorithm need to come from sources that are too rich and complex to treat algorithmically or through some multi-dimensional analysis of hidden regularities (like deep neural nets). The inputs require either a fairly general artificial intelligence (although not full blown AGI) or that everyone keeps their calendar in the same way. (Even then we’d probably have to deal with travelling-salesman problems – but at least we have some ideas about the limits on the computability of those.)

There are many individual components of this process that could be algorithmically assisted. But often the simpler algorithms and heuristics such as preference polls and shared calendars are more effective aids than opaque machine learning output.

So although, this looks like a problem that should be solvable through ML, early attempts have been less than impressive.

3. Importing data about people into a table (deduplication)
-----------------------------------------------------------

Computers are great as aids to managing structured data. But the input into the structure has to be provided by humans. Can AI help here?

Imagine you’re organising an event and you want people to tell you if they’re coming. You can just ask and keep in your head who said yes. But that soon becomes too much. As a next step, you ask them to email or to send an RSVP so you can look at the messages and remind yourself who said yes. But even that becomes difficult soon, so you start a list. And the more people and events you need to manage, the more complicated the list is and the more time you have to spend structuring your data and inputing it into some sort of a table for managing and reviewing the data.

The world is littered with Excel sheets kept by event organisers. Now imagine you wanted to feed all the idiosyncratic Excel sheets with event information at a large organisation into a machine learning algorithm and get one number of the total number of participants or the total cost of lunch breaks.

If everybody kept their spreadsheets exactly the same way, this would be trivial. But they don’t. Computers make the task of managing this kind of structured data much easier but they constantly struggle with errors in the input from busy, overworked and cognitively limited humans.

On the surface of it, there’s nothing to prevent this part (ie participant registration and management) of event management from being completely automated. But there’s always a person involved in dealing with this. So could there be an AI system that does all of this? So far we’re not even very close to this. A system that processes some RSVPs via email, others via forms, and others from other sources (“Hi, Clare, Frances told me she was coming to your party!”) does not exist.

So let’s simplify the task even more. Take data from one table of a system (let’s say a registration table) and put it into another table on a different system (let’s say account creation). All the AI system would have to do is figure out what is important to one system and get the right data from another system. At the moment, humans are involved. In better cases by creating an API and programming algorithms to transfer data between systems. In the worse case, they download a spreadsheet from one system, modify it, if needed, and upload it into another system.

This is trivial if you’ve designed both systems and know they have to integrate. But the permutations get out of hand surprisingly quickly when you take any 2 random systems designed by different people for a similar purpose but without the intention to integrate. Is ‘Last name’ always the ‘Second name’, when the full name is in one column, is first name always first? Any one difficulty is easy to spot for a human and disambiguate. But it gets very error prone at scale and there are always some unexpected edge cases.

Even such a simple thing as contact deduplication between two devices of one person is not a completely solved problem.

Why isn’t there an AI system that can evaluate the data and transfer it as appropriate but at scale and without the errors human data processors or programmers or data processing algorithms make?

As always, even the most trivial algorithms require very complex inputs. And with even minor variation in the possible inputs, the if-then logic becomes too unweildy. Although computers in general are great at pursuing if-then logic chains regardless of complexity (within limits), AI algorithms are not. They provide guesses with probabilities. In certain areas, most notably speech and image recognition, their guesses are becoming very good and resembling humans. They may even outperform humans at scale.

But all the if-then part of what to do with these guesses is still handled by if-then algorithms designed by humans. There’s some talk of ‘Programming 2.0’ but nobody seems to be applying it to some of the day-to-day simple problems with complex scaling. Because even small errors in the inputs result in big aggregate problems and AI systems have no way of assessing whether their guesses ‘make sense’.

Is AI impossible?
-----------------

Maybe AI is just too hard. But these examples don’t claim it’s impossible, they just show that some difficult problems are just difficult. Even if they appear straightforward on the surface.

I have learned not to bet against engineers’ ability to figure out solutions in the long run. It’s not always clear what is solvable by AI and what is not ahead of time. Sometimes, specialised ML systems can be developed to solve problems that don’t generalise (e.g. GO or chess machines). But I would have expected more people to deal with these problems, if there was an easy solution to be found. And there hundreds more similar task-based problems that just won’t be magicked away by slapping the label ‘AI’ on it. Individual ones may be solved by one way or another. Perhaps by breaking them into component parts. But I’m not seeing any specific steps being taken to create general purpose Machine Learning that would deal with all of them. Just wishful thinking about AGI (Artificial General Intelligence) emerging to solve these problems without regard to the actual complexity of some of them or the complexity of the intermediate steps it would take to get there.

### *Related*
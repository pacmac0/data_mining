import os
import codecs
import string

class Preprocessor:
    def __init__(self, \
                 TEXT_DIR = "dataset/sportsArticles/raw_data", \
                 MAX_DOC_COUNT = 100, \
                 lower_case=True, \
                 norm_spaces=True, \
                 punctuation=True):
        self.TEXT_DIR = TEXT_DIR
        self.MAX_DOC_COUNT = MAX_DOC_COUNT
        self.lower_case = lower_case
        self.norm_spaces = norm_spaces
        self.punctuation = punctuation

        self.corpus = []

    def load_texts_from_dir(self):
        for count, file_name in enumerate(os.listdir(self.TEXT_DIR)):
            if count < self.MAX_DOC_COUNT:
                file_path = self.TEXT_DIR+"/"+file_name
                with codecs.open(file_path, 'r', 'ISO-8859-1') as text_file:
                    text = reader = str(text_file.read())
                    clean_text = self.clean_text(text)
                    self.corpus.append(clean_text)

    def clean_text(self, txt):
        if self.lower_case:
            txt = txt.lower()
        if self.norm_spaces:
            txt = ' '.join(txt.split()) # split recognizes all types of whitespaces
        if self.punctuation:
            txt = ''.join(c for c in txt if c not in string.punctuation)
        return txt

    def load_test_cases(self):
        # original
        text1 = """
        Nadal was named Sportsman of the Year after a remarkable season in which he won the French Open, Wimbledon and US Open trophies while Spain's World Cup side were named Team of the Year at a glittering ceremony attended by celebrities and sporting greats.
        "It's an honour, in my name, that of my colleagues and the Spanish football federation, to receive this award from the world of sport," Spain coach Vicente del Bosque said in a live feed to the awards ceremony from the team's training base outside Madrid.
        American Alpine skier Lindsay Vonn, who won the Olympic downhill gold at the Vancouver Games last February just days after suffering a shin injury, was voted Sportswoman of the Year.
        Spain, the USA and Germany were the big winners with each country bagging two awards.
        
        There was a rapturous welcome for French football great Zinedine Zidane, who received the Lifetime Achievement Award in recognition of his remarkable career.
        The Spirit of Sport Award was presented to the European Ryder Cup Team to mark their emotional win over the United States in a match "which demonstrated great sportsmanship, golf played at the highest level and enormous and passionate galleries", a statement from the organisers said.
        The Laureus World Sports Awards, which recognise sporting achievement, are the premier honours on the international sporting calendar.
        Double Oscar winner Kevin Spacey hosted the event attended by celebrities from the world of sports and entertainment.
        The award winners were: 
        Laureus World Sportsman of the Year: Rafael Nadal (Spain) 
        Laureus World Sportswoman of the Year: Lindsey Vonn (US) 
        Laureus World Team of the Year: Spain World Cup 
        Team Laureus World Breakthrough of the Year: Martin Kaymer (Germany) 
        Laureus World Comeback of the Year: Valentino Rossi (Italy) 
        Laureus World Sportsperson of the Year with a Disability: Verena Bentele (Germany) 
        Laureus World Action Sportsperson of the Year: Kelly Slater (US)
        """
        self.corpus.append(self.clean_text(text1))
        text_extra_word = """
        EXTRA Nadal was named Sportsman of the Year after a remarkable season in which he won the French Open, Wimbledon and US Open trophies while Spain's World Cup side were named Team of the Year at a glittering ceremony attended by celebrities and sporting greats.
        "It's an honour, in my name, that of my colleagues and the Spanish football federation, to receive this award from the world of sport," Spain coach Vicente del Bosque said in a live feed to the awards ceremony from the team's training base outside Madrid.
        American Alpine skier Lindsay Vonn, who won the Olympic downhill gold at the Vancouver Games last February just days after suffering a shin injury, was voted Sportswoman of the Year.
        Spain, the USA and Germany were the big winners with each country bagging two awards.
        
        There was a rapturous welcome for French football great Zinedine Zidane, who received the Lifetime Achievement Award in recognition of his remarkable career.
        The Spirit of Sport Award was presented to the European Ryder Cup Team to mark their emotional win over the United States in a match "which demonstrated great sportsmanship, golf played at the highest level and enormous and passionate galleries", a statement from the organisers said.
        The Laureus World Sports Awards, which recognise sporting achievement, are the premier honours on the international sporting calendar.
        Double Oscar winner Kevin Spacey hosted the event attended by celebrities from the world of sports and entertainment.
        The award winners were: 
        Laureus World Sportsman of the Year: Rafael Nadal (Spain) 
        Laureus World Sportswoman of the Year: Lindsey Vonn (US) 
        Laureus World Team of the Year: Spain World Cup 
        Team Laureus World Breakthrough of the Year: Martin Kaymer (Germany) 
        Laureus World Comeback of the Year: Valentino Rossi (Italy) 
        Laureus World Sportsperson of the Year with a Disability: Verena Bentele (Germany) 
        Laureus World Action Sportsperson of the Year: Kelly Slater (US)
        """
        self.corpus.append(self.clean_text(text_extra_word))
        text2 = """
        Nadal was named Spodrtsman of the Year after a remadrkable season in which he won the French Open, Wimbledon and US Open trophies while Spain's World Cup side were named Team of the Year at a glittering ceremony attended by celebrities and sporting greats.
        "It's an honour, ddin my nadme, that of my codlleagues and the dSpanish football dfederation, to receive this award from the world of sport," Spain coach Vicente del Bosque said in a live feed to the awards ceremony from the team's training base outside Madrid.
        American Alpine skier Lindsay Vonnd, who won the Olympic downhill gold at the Vancouver Games last February just days after suffering a shin injury, was voted Sportswoman of the Year.
        Spain, the USA and Germany were the big dwinners with each country bagging two awards.
        dd
        There was a rapturous welcome for French football great Zinedine Zidane, who received the Lifetime Achievement Award in recognition of his remarkable career.
        The Spirit of Sport Award was presendted to the European Ryder Cup Team to dmark their emotional win over the United States in a match "which demonstrated great sportsmanship, golf played at the highest level and enormous and passionate galleries", a statement from the organisers said.
        The Laureus World Sports Awaasdrds, which recogdnise sporting achievement, are the premier honours on the international sporting calendar.
        Double Oscar winner Kevind Spacey hosted the event attended by celebrities from the world of sports and entertainment.
        The award winners were: 
        Laureus World Sportsman of the Year: Rafael Nadal (Spain) 
        Laureus World Sportdswoman of the Year: Lindsedy Vonn (US) 
        Laureusd Wordddld Team of the Year: Spain World Cup 
        Team Laureus Wdorld Breakthrough of the Yeadr: Martin Kaymer (Germany) 
        Laureusd World Comeback of the Year: Valentino Rossi (Italy) 
        Laureus World Sportdspersodn of the Year with a Disability: Verena Bentele (Germany) 
        Laureus World Actiond Sportsperson of the Year: dKelly Slater (US)
        """
        self.corpus.append(self.clean_text(text2))
        text_l = """
        Nadal was named Sportsman of the Year after a remarkable season in which he won the French Open, Wimbledon and US Open trophies while Spain's World Cup side were named Team of the Year at a glittering ceremony attended by celebrities and sporting greats.
        "It's an honour, in my name, that of my colleagues and the Spanish football federation, to receive this award from the world of sport," Spain coach Vicente del Bosque said in a live feed to the awards ceremony from the team's training base outside Madrid.
        American Alpine skier Lindsay Vonn, who won the Olympic downhill gold at the Vancouver Games last February just days after suffering a shin injury, was voted Sportswoman of the Year.
        Spain, the USA and Germany were the big winners with each country bagging two awards.
  
        There was a rapturous welcome for French football great Zinedine Zidane, who received the Lifetime Achievement Award in recognition of his remarkable career.
        The Spirit of Sport Award was presented to the European Ryder Cup Team to mark their emotional win over the United States in a match "which demonstrated great sportsmanship, golf played at the highest level and enormous and passionate galleries", a statement from the organisers said.
        The Laureus World Sports Awards, which recognise sporting achievement, are the premier honours on the international sporting calendar.
        Double Oscar winner Kevin Spacey hosted the event attended by celebrities from the world of sports and entertainment.
        The award winners were: 
        Laureus World Sportsman of the Year: Rafael Nadal (Spain) 
        Laureus World Sportswoman of the Year: Lindsey Vonn (US) 
        Laureus World Team of the Year: Spain World Cup 
        Team Laureus World Breakthrough of the Year: Martin Kaymer (Germany) 
        Laureus World Comeback of the Year: Valentino Rossi (Italy) 
        Laureus World Sportsperson of the Year with a Disability: Verena Bentele (Germany) 
        Laureus World Action Sportsperson of the Year: Kelly Slater (US)

        Added some text just to make the document longer and see how this influences the similarity.
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vitae turpis nec tortor faucibus facilisis.
        Aliquam vitae massa facilisis, aliquam mauris nec, gravida massa. Suspendisse tellus odio, condimentum at blandit vel, euismod a nunc. 
        Vestibulum tempor lacus risus, id elementum dui pulvinar non.
        Vestibulum metus libero, placerat nec venenatis vitae. 
        """
        self.corpus.append(self.clean_text(text_l))
        text_s = """
        There was a rapturous welcome for French football great Zinedine Zidane, who received the Lifetime Achievement Award in recognition of his remarkable career.
        The Spirit of Sport Award was presented to the European Ryder Cup Team to mark their emotional win over the United States in a match "which demonstrated great sportsmanship, golf played at the highest level and enormous and passionate galleries", a statement from the organisers said.
        The Laureus World Sports Awards, which recognise sporting achievement, are the premier honours on the international sporting calendar.
        Double Oscar winner Kevin Spacey hosted the event attended by celebrities from the world of sports and entertainment.
        The award winners were: 
        Laureus World Sportsman of the Year: Rafael Nadal (Spain) 
        Laureus World Sportswoman of the Year: Lindsey Vonn (US) 
        Laureus World Team of the Year: Spain World Cup 
        Team Laureus World Breakthrough of the Year: Martin Kaymer (Germany) 
        Laureus World Comeback of the Year: Valentino Rossi (Italy) 
        Laureus World Sportsperson of the Year with a Disability: Verena Bentele (Germany) 
        Laureus World Action Sportsperson of the Year: Kelly Slater (US)
        """
        self.corpus.append(self.clean_text(text_s))
        text3="""
        Carmelo Anthony wasted little time letting his frustration be known after the New York Knicks’ 102-96 loss to the Boston Celtics on Monday night. In fact, Anthony apparently was so worked up over his team’s sixth defeat in 11 games that he wanted to let his Atlantic Division rivals know first-hand.
        Following his 6-of-26 shooting performance, one of the worst of his career, the Knicks star was reportedly involved in an exchange outside the visitors locker room at Madison Square Garden, possibly with Celtics forward Kevin Garnett, with whom he had several dust-ups during the hotly contested game — one resulting in double-technical fouls for the two All-Stars.
        After the game, no one in either locker room would confirm the report, though the players wouldn’t necessarily deny it either. Conveniently, everyone was clueless as to what had or hadn’t gone on. But every indication — the coy smiles, the careful, overwrought language — said that something had gone down.
        
        Check out the FOXiest NBA fans and tweet us your photo.
    
        What? We may never know for sure, though a Comcast Sports New England video showed Anthony pacing and waiting for KG near the Celtics’ team bus. That’s all there is to go on for now.
        “I’m going to let you all figure that out,” said Celtics coach Doc Rivers, who saw his team win its third straight game after losing eight of 10 between Dec. 14 and Jan. 2. “I’m going to stay out of that. If it was the playoffs, I’d tell on him, but since it’s not, I’m going to just be quiet.”
        When pressed, Garnett (19 points, 10 rebounds) was equally coy (not that he’s ever overly forthright when it comes to such matters) and brushed the maybe-disturbance off as “just basketball.” And ‘Melo himself — well, he left without addressing the media after the game, his empty locker doing the speaking for him as his silence said more than he ever would have, anyway.
        Paul Pierce, who led the Celtics with 23 points, wasn’t about to be goaded into dishing on the fracas, nor was Avery Bradley, who played the stingiest defense the Knicks have seen in some time. Bradley also scored 13 points in place of Rajon Rondo, who had been suspended by the league for contact with an official in Sunday’s win over Atlanta.
        
        Most around the Knicks locker room were, unsurprisingly, somewhere else at the time of the quarrel — J.R. Smith (24 points) was getting 11 stitches above his right eye; Amar’e Stoudemire (13 points) was getting treatment on his knee; and Marcus Camby and Steve Novak didn’t recall where they were, but they definitely weren’t in the hallway trying to hold ‘Melo back.
        Wink, wink.
        “‘Melo’s a very fiery guy, believe it or not,” Smith said. “He doesn’t like to lose, and he doesn’t like when people try to come up in his face. It is what it is.”
        Added Novak: “We’re at home and we expect to win, he (Anthony) expects to win. And I think it’s healthy, I think it’s good. I think that he puts a lot of importance on all these games. He doesn’t take it lightly, and I think that’s what you want to see out of your leader.”
        Though the details of the dust-up are scarce, and may remain that way, it’s clear Anthony let Garnett and the Celtics get the best of him Monday. But at least Anthony can take comfort in the knowledge that, over the last week, Boston has burned just about everyone during a mini-revival following the team’s challenging run through December.
        On Friday and Saturday, Boston (17-17) logged convincing wins over Atlanta and Indiana, the third- and fourth-seeded teams in the Eastern Conference, respectively, before heading to New York for Monday’s win over the second-seeded Knicks. Monday’s win came just in time for the Celtics’ return to TD Garden for a five-game homestand.
        “The last three games have been terrific,” Rivers said. “When you’ve got Indiana and Atlanta back-to-back and then you play the Knicks after that, and to win all three of those games, that’s great for our team. Winning this game here, without Rondo, just tells you our guys hung in there.”
        Though Boston played solid offensively against the Knicks, who have made their name on defense this season, it was their defense that owned the night. The Celtics held New York to 40.8 percent shooting from the floor and have limited opponents to 37.5 percent shooting during their three-game win streak as they’ve looked a lot like the title-contending Celtics of old.
        “We’re defending a whole lot better,” Pierce said. “We’re putting more pressure on teams, we’re rebounding the ball a lot better, we’re moving the ball, and this is the type of the ball we envisioned when we came together. Hopefully we can keep it going.”
        
        The Celtics’ recent success has propelled them to the No. 7 seed in the watered-down East as of Monday night, and has also helped deflect some attention away from their worrisome start so far. Looking old and slow and completely out of sync for most of the season before January, Boston was finding itself with few answers for its growing list of problems.
        Between their poor play, Rondo’s poor attitude and the recent, familiar trade rumors surrounding the team — the latest involving the Kings’ Demarcus Cousins — the Celtics’ situation had grown tenuous over the last few weeks. Perhaps their only saving grace has been a train wreck of a Lakers team that has stolen most of the negative press that would have normally descended upon Boston.
        The heat won’t be totally off the Celtics unless they can continue to play like the team that we’ve come to expect over the years, but this week’s brief reprieve may be helpful on many levels going forward.
        “It’s what we can be but it’s not what we’ve been, and that’s what I’ve been saying,” Rivers said when asked if Monday’s performance met his expectations for his club. “We can be better, but it’s a start.”
        Anthony, meanwhile, didn’t get to finish what he apparently intended to start on Monday, but he’ll certainly get his chance on Jan. 24, when the teams meet again at Madison Square Garden.
        
        “In the heat of the battle, man, guys go back and forth,” Garnett said. “(Anthony is) trying to get his team to go, I’m trying to get my team to go. Both teams are colliding, not to mention it’s the Knicks and the Celtics.”
        Added Rivers: “There’s nothing wrong with getting heated, it happens. It’s just a fun game, it’s competitive, it’s rough at times, and that’s good. I think all that’s good. It shouldn’t ever carry over past that — I’ve had my moments as a player, as well — and it does, but you don’t want it to.”
        You can follow Sam Gardner on Twitter or email him at samgardnerfox@gmail.com.
        """
        self.corpus.append(self.clean_text(text3))
        text3_diff="""
        Carmelo Anthony wasted little time letting his frustration be known after the New York Knicks’ 102-96 loss to the Boston Celtics on Monday night. In fact, Anthony apparently was so worked up over his team’s sixth defeat in 11 games that he wanted to let his Atlantic Division rivals know first-hand.
        Following his 6-of-26 shooting performance, one of the worst of his career, the Knicks star was reportedly involved in an exchange outside the visitors locker room at Madison Square Garden, possibly with Celtics forward Kevin Garnett, with whom he had several dust-ups during the hotly contested game — one resulting in double-technical fouls for the two All-Stars.
        
        Check out the FOXiest NBA fans and tweet us your photo.
    
        What? We may never know for sure, though a Comcast Sports New England video showed Anthony pacing and waiting for KG near the Celtics’ team bus. That’s all there is to go on for now.
        When pressed, Garnett (19 points, 10 rebounds) was equally coy (not that he’s ever overly forthright when it comes to such matters) and brushed the maybe-disturbance off as “just basketball.” And ‘Melo himself — well, he left without addressing the media after the game, his empty locker doing the speaking for him as his silence said more than he ever would have, anyway.
        Paul Pierce, who led the Celtics with 23 points, wasn’t about to be goaded into dishing on the fracas, nor was Avery Bradley, who played the stingiest defense the Knicks have seen in some time. Bradley also scored 13 points in place of Rajon Rondo, who had been suspended by the league for contact with an official in Sunday’s win over Atlanta.
        
        Most around the Knicks locker room were, unsurprisingly, somewhere else at the time of the quarrel — J.R. Smith (24 points) was getting 11 stitches above his right eye; Amar’e Stoudemire (13 points) was getting treatment on his knee; and Marcus Camby and Steve Novak didn’t recall where they were, but they definitely weren’t in the hallway trying to hold ‘Melo back.
        Wink, wink.
        “‘Melo’s a very fiery guy, believe it or not,” Smith said. “He doesn’t like to lose, and he doesn’t like when people try to come up in his face. It is what it is.”
        Added Novak: “We’re at home and we expect to win, he (Anthony) expects to win. And I think it’s healthy, I think it’s good. I think that he puts a lot of importance on all these games. He doesn’t take it lightly, and I think that’s what you want to see out of your leader.”
        Though the details of the dust-up are scarce, and may remain that way, it’s clear Anthony let Garnett and the Celtics get the best of him Monday. But at least Anthony can take comfort in the knowledge that, over the last week, Boston has burned just about everyone during a mini-revival following the team’s challenging run through December.
        On Friday and Saturday, Boston (17-17) logged convincing wins over Atlanta and Indiana, the third- and fourth-seeded teams in the Eastern Conference, respectively, before heading to New York for Monday’s win over the second-seeded Knicks. Monday’s win came just in time for the Celtics’ return to TD Garden for a five-game homestand.
        “The last three games have been terrific,” Rivers said. “When you’ve got Indiana and Atlanta back-to-back and then you play the Knicks after that, and to win all three of those games, that’s great for our team. Winning this game here, without Rondo, just tells you our guys hung in there.”
        “We’re defending a whole lot better,” Pierce said. “We’re putting more pressure on teams, we’re rebounding the ball a lot better, we’re moving the ball, and this is the type of the ball we envisioned when we came together. Hopefully we can keep it going.”
        
        The Celtics’ recent success has propelled them to the No. 7 seed in the watered-down East as of Monday night, and has also helped deflect some attention away from their worrisome start so far. Looking old and slow and completely out of sync for most of the season before January, Boston was finding itself with few answers for its growing list of problems.
        Between their poor play, Rondo’s poor attitude and the recent, familiar trade rumors surrounding the team — the latest involving the Kings’ Demarcus Cousins — the Celtics’ situation had grown tenuous over the last few weeks. Perhaps their only saving grace has been a train wreck of a Lakers team that has stolen most of the negative press that would have normally descended upon Boston.
        The heat won’t be totally off the Celtics unless they can continue to play like the team that we’ve come to expect over the years, but this week’s brief reprieve may be helpful on many levels going forward.
        “It’s what we can be but it’s not what we’ve been, and that’s what I’ve been saying,” Rivers said when asked if Monday’s performance met his expectations for his club. “We can be better, but it’s a start.”
        Anthony, meanwhile, didn’t get to finish what he apparently intended to start on Monday, but he’ll certainly get his chance on Jan. 24, when the teams meet again at Madison Square Garden.
        
        “In the heat of the battle, man, guys go back and forth,” Garnett said. “(Anthony is) trying to get his team to go, I’m trying to get my team to go. Both teams are colliding, not to mention it’s the Knicks and the Celtics.”
        You can follow Sam Gardner on Twitter or email him at samgardnerfox@gmail.com.
        """
        self.corpus.append(self.clean_text(text3_diff))
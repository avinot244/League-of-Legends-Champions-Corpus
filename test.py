from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers.models.t5.modeling_t5 import T5ForConditionalGeneration
from transformers.models.t5.tokenization_t5_fast import T5TokenizerFast
import torch
import json

def token_length(word : str, tokenizer):
    return len(tokenizer.tokenize(word))

def split_text(text : str, tokenizer : AutoTokenizer, max_length : int = 350):
    
    res : list[str] = []
    sentence_list : list[str] = text.split(".")
    
    chunk : str = ""
    for sentence in sentence_list:
        if token_length(chunk, tokenizer) + token_length(sentence, tokenizer) < max_length:
            chunk += f"{sentence}."
        else:
            res.append(chunk)
            chunk = ""
    res.append(chunk)
    return res

def propositionizer(title : str, section : str, content : str) -> list[str]:
    model_name = "chentong00/propositionizer-wiki-flan-t5-large"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    print(type(tokenizer))

    splitted_content : list[str] = split_text(content, tokenizer)
    

    res : list[str] = []
    
    for content_split in splitted_content:
        if content_split[0] == " ":
            input_text = f"Title: {title}. Section: {section}. Content: {content_split[1:]}"
        else:
            input_text = f"Title: {title}. Section: {section}. Content: {content_split}"
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids
        outputs = model.generate(input_ids.to(device), max_new_tokens=512).cpu()
        
        output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        try:
            prop_list = json.loads(output_text)
            res += prop_list
        except:
            print(input_text)
            print(output_text)
            prop_list = []
            print("[ERROR] Failed to parse output text as JSON.")
        
        
    return res

content : str = "Why play Udyr Top? Well, he is incredibly versatile. He has many strong matchups, he deals great AoE damage, and he has amazing built-in sustain. However, he is reliant on his passive which has a long cooldown, and his entire kit is predictable basically just running at your opponent. Udyr's passive is he has no ultimate ability but has 4 basic abilities instead which changes stance. Additionally, he can periodically empower one of his abilities and will come to what each empowerment does with each ability. In addition, when changing stances he empowers his next two basic attacks to gain bonus attack speed and refund some of his passive. Udyr's Q isn't important as we don't level it. Udyr's W grants him a shield and makes his next two attacks gain lifesteal and heal him. The empowered version increases his shield strength and grants him healing. It also grants him double the normal lifesteal and healing of his next two attacks. Udyr's E causes him to become ghosted and gain bonus movement speed. In addition, it empowers his next basic attacks to pounce on the target and stun them. When empowered, he gains even more bonus attack range and bonus speed, and he becomes immune to CC for a short amount of time. His R ability creates a circle around him which deals damage to all enemies within and slows them. And it empowers his next 2 attacks to deal bonus splash damage. The empowered version causes the storm to chase the target, dealing even more damage and having a better slow. For combos, engage with E into 2 attacks, into R into attacks, into W into attacks. This will be your basic combo and you'll enhance whichever ability you need. If you need to run through crowd control, you want to empower your E, if you want even more damage, you'll empower your R, and if you want to be tankier you empower your W. Of course making sure you use two attacks between each ability. For matchups, Udyr is amazing into tanky top lane bruises who he can simply outvalue in extended fights. And he can struggle against some of the higher damage carries in the top lane who can take him down before his kit gives him too much value. For runes take this, grasp is great as you want to keep going in. For build orders, start ringing pots into an Iceborne Gauntlet and tier 2 boots. After this, a frozen heart and canik rook can a great pickups before finishing your build with any of these as needed. For skill orders, start R than W than E before maxing R than W than E. For summoner spells, take Ghost and Teleport. Starting the game, ask the top laner you're looking to farm heart and take good trades. Udi has access to some amazing trading patterns. Your E giving you the speed up and the dash stun lets you choose a lot of fights. And you only want to be choosing these fights when you have access to empowering your ability. From here, you need to choose whether to empower your R for more damage or your W for more sustain. Often into tanks you'll empower your R ability and against high damage threats you'll empower your W. The longer the fight goes, the more you'll be rotating through your stances and getting your passive hits off, so the longer the fight, the more value you tend to get. However, at level 6 you don't get the big power spike so do care against champions that do. Enter in the mid game, take your tower as soon as possible and look to push your lane out as far as you can safely. After this you can split push or you can just simply group up with your team for fights and objectives. Entering late game team fights, you want to play as the front line champion. Stay in the front line and stun anything going for your back line while passively dealing tons of damage with your art ability, especially if you can empower this ability to stick onto their team. If the opportunity comes up, you can jump onto their back line, stun them and pile damage into them, otherwise just keep damaging their front line."

# content : str = "For combos, engage with E into 2 attacks, into R into attacks, into W into attacks. This will be your basic combo and you'll enhance whichever ability you need. If you need to run through crowd control, you want to empower your E, if you want even more damage, you'll empower your R, and if you want to be tankier you empower your W. Of course making sure you use two attacks between each ability. For matchups, Udyr is amazing into tanky top lane bruises who he can simply outvalue in extended fights. And he can struggle against some of the higher damage carries in the top lane who can take him down before his kit gives him too much value. For runes take this, grasp is great as you want to keep going in. For build orders, start ringing pots into an Iceborne Gauntlet and tier 2 boots. After this, a frozen heart and canik rook can a great pickups before finishing your build with any of these as needed. For skill orders, start R than W than E before maxing R than W than E. For summoner spells, take Ghost and Teleport. Starting the game, ask the top laner you're looking to farm heart and take good trades. Udi has access to some amazing trading patterns. Your E giving you the speed up and the dash stun lets you choose a lot of fights. And you only want to be choosing these fights when you have access to empowering your ability."


title : str = "Udyr"

res = propositionizer(title, "", content)
print(json.dumps(res, indent=4))

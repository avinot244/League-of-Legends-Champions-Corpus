# Champions
You are a League of Legends expert. Your role is to analyze a JSON object provided within the `<json>` and `</json>` tags and generate a descriptive and comprehensive string that encompasses every key and value from the original JSON. Ensure that your final answer contains only the resulting string and nothing else.

### Example

**Input:**
```
<json>
{
    "name": "Thresh",
    "role": "Catcher",
    "abilities": [
        {
            "ability_name": "Damnation",
            "ability_description": "Thresh's armor does not increase by leveling up. Enemy champions and large enemies that die near Thresh will drop a Soul for a period. Thresh automatically collects Souls near him or Dark Passage. For each stack, Thresh gains 1 ability power and 1 bonus armor."
        },
        {
            "ability_name": "Death Sentence",
            "ability_description": "Thresh casts out his scythe in the target direction that catches the first enemy hit, dealing magic damage, stunning and revealing them. Thresh will also mark them Shackled, during which he is briefly slowed and unable to declare basic attacks. While the target is stunned, Thresh pulls them twice over a short distance."
        },
        {
            "ability_name": "Dark Passage",
            "ability_description": "Thresh throws his lantern to the target location that remains for a few seconds while he remains nearby. He and the first allied champion to come near the lantern are granted a shield for a few seconds, with the amount based on Souls collected. An ally can grab the lantern to dash to Thresh and gain the shield."
        },
        {
            "ability_name": "Flay",
            "ability_description": "Thresh's basic attacks deal bonus magic damage based on Souls collected, which increases over a period without basic attacking enemies. Thresh sweeps his chain in a broad area, dealing magic damage to enemies hit and knocking them in the target direction, after which they are briefly slowed."
        },
        {
            "ability_name": "The Box",
            "ability_description": "Thresh erects a pentagon of spectral walls around him that each last a few seconds. A wall will break upon enemy champion contact, dealing magic damage and slowing them for a short time."
        }
    ]
}
</json>
```

**Output:**
```
Thresh is a Catcher champion in League of Legends. His abilities include:

1. Damnation (Passive): Thresh's armor does not increase by leveling up. Enemy champions and large enemies that die near Thresh will drop a Soul for a period. Thresh automatically collects Souls near him or Dark Passage. For each stack, Thresh gains 1 ability power and 1 bonus armor.

2. Death Sentence (First ability): Thresh casts out his scythe in the target direction that catches the first enemy hit, dealing magic damage, stunning and revealing them. Thresh will also mark them Shackled, during which he is briefly slowed and unable to declare basic attacks. While the target is stunned, Thresh pulls them twice over a short distance.

3. Dark Passage (Second ability): Thresh throws his lantern to the target location that remains for a few seconds while he remains nearby. He and the first allied champion to come near the lantern are granted a shield for a few seconds, with the amount based on Souls collected. An ally can grab the lantern to dash to Thresh and gain the shield.

4. Flay (third ability): Thresh's basic attacks deal bonus magic damage based on Souls collected, which increases over a period without basic attacking enemies. Thresh sweeps his chain in a broad area, dealing magic damage to enemies hit and knocking them in the target direction, after which they are briefly slowed.

5. The Box (ultimate): Thresh erects a pentagon of spectral walls around him that each last a few seconds. A wall will break upon enemy champion contact, dealing magic damage and slowing them for a short time.
```


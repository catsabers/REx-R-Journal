   

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class Tier(Enum):
                          
    LAYER = "Layer"
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    MASTER = "Master"
    SURREAL = "Surreal"
    MYTHIC = "Mythic"
    EXOTIC = "Exotic"
    EXQUISITE = "Exquisite"
    TRANSCENDENT = "Transcendent"
    ENIGMATIC = "Enigmatic"
    UNFATHOMABLE = "Unfathomable"
    OTHERWORLDLY = "Otherworldly"
    ZENITH = "Zenith"
    EXCLUSIVE = "Exclusive"


@dataclass
class Ore:
                                             
    name: str
    world: str
    layer: str
    tier: Tier
    rarity_value: int = 0                                                 
    is_cave_exclusive: bool = False
    cave_type: Optional[str] = None                                                                 
    
    def __str__(self):
        return self.name

    @property
    def key(self) -> str:
           
        return f"{self.world}::{self.layer}::{self.name}"
    
    def to_dict(self) -> Dict:
                                                              
        return {
            "name": self.name,
            "world": self.world,
            "layer": self.layer,
            "tier": self.tier.value,
            "rarity_value": self.rarity_value,
            "is_cave_exclusive": self.is_cave_exclusive,
            "cave_type": self.cave_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Ore':
                                        
        return cls(
            name=data["name"],
            world=data["world"],
            layer=data["layer"],
            tier=Tier(data["tier"]),
            rarity_value=data.get("rarity_value", 0),
            is_cave_exclusive=data.get("is_cave_exclusive", False),
            cave_type=data.get("cave_type", None)
        )


class OreDatabase:
                                        
    
    def __init__(self):
        self.ores: List[Ore] = []
        self._initialize_ores()
    
    def _initialize_ores(self):
           
        self.ores = []
        
                       
                                                                                                         
        self.ores.append(Ore("Aegistone", "Natura", "Stone Layer", Tier.EXOTIC, rarity_value=2820000))
        self.ores.append(Ore("Scertanium", "Natura", "Stone Layer", Tier.EXOTIC, rarity_value=3524000))
        self.ores.append(Ore("Penumbrosia", "Natura", "Stone Layer", Tier.EXQUISITE, rarity_value=9125550))
        self.ores.append(Ore("Pasivium", "Natura", "Stone Layer", Tier.TRANSCENDENT, rarity_value=21210000))
        self.ores.append(Ore("Pastelorium", "Natura", "Stone Layer", Tier.TRANSCENDENT, rarity_value=44300000))
        self.ores.append(Ore("Gradience", "Natura", "Stone Layer", Tier.ENIGMATIC, rarity_value=61345755))
        self.ores.append(Ore("Vaporwave Crystal", "Natura", "Stone Layer", Tier.ENIGMATIC, rarity_value=90000000))
        self.ores.append(Ore("Endozivite", "Natura", "Stone Layer", Tier.UNFATHOMABLE, rarity_value=247010000))
        
                                        
        self.ores.append(Ore("Freon", "Natura", "Basalt Layer", Tier.EXOTIC, rarity_value=3333333))
        self.ores.append(Ore("Snoblintium", "Natura", "Basalt Layer", Tier.EXOTIC, rarity_value=4220000))
        self.ores.append(Ore("Nauticalis", "Natura", "Basalt Layer", Tier.EXQUISITE, rarity_value=12221221))
        self.ores.append(Ore("Azuryl", "Natura", "Basalt Layer", Tier.TRANSCENDENT, rarity_value=26700000))
        self.ores.append(Ore("Glacielle", "Natura", "Basalt Layer", Tier.TRANSCENDENT, rarity_value=31400000))
        self.ores.append(Ore("Bulbalescense", "Natura", "Basalt Layer", Tier.ENIGMATIC, rarity_value=81818181))
        self.ores.append(Ore("Cybernetium", "Natura", "Basalt Layer", Tier.ENIGMATIC, rarity_value=52400000))
        self.ores.append(Ore("Inclemetite", "Natura", "Basalt Layer", Tier.UNFATHOMABLE, rarity_value=386500000))
        
                                         
        self.ores.append(Ore("Astatine", "Natura", "Granite Layer", Tier.EXOTIC, rarity_value=4200000))
        self.ores.append(Ore("Elexinite", "Natura", "Granite Layer", Tier.EXOTIC, rarity_value=2120000))
        self.ores.append(Ore("Elegascene", "Natura", "Granite Layer", Tier.EXQUISITE, rarity_value=13902340))
        self.ores.append(Ore("Oviridis", "Natura", "Granite Layer", Tier.EXQUISITE, rarity_value=9239085))
        self.ores.append(Ore("Erodimium", "Natura", "Granite Layer", Tier.TRANSCENDENT, rarity_value=35900000))
        self.ores.append(Ore("Spristium", "Natura", "Granite Layer", Tier.TRANSCENDENT, rarity_value=21500000))
        self.ores.append(Ore("Candilium", "Natura", "Granite Layer", Tier.ENIGMATIC, rarity_value=82000000))
        self.ores.append(Ore("Runealith", "Natura", "Granite Layer", Tier.ENIGMATIC, rarity_value=55299490))
        self.ores.append(Ore("Terratomere", "Natura", "Granite Layer", Tier.UNFATHOMABLE, rarity_value=213200000))
        
                                         
        self.ores.append(Ore("Monocage", "Natura", "Diorite Layer", Tier.EXOTIC, rarity_value=5000000))
        self.ores.append(Ore("Neptunium", "Natura", "Diorite Layer", Tier.EXOTIC, rarity_value=4390000))
        self.ores.append(Ore("Acceleratium", "Natura", "Diorite Layer", Tier.EXQUISITE, rarity_value=7820000))
        self.ores.append(Ore("Lucidium", "Natura", "Diorite Layer", Tier.TRANSCENDENT, rarity_value=43211234))
        self.ores.append(Ore("Quandrium", "Natura", "Diorite Layer", Tier.TRANSCENDENT, rarity_value=29290000))
        self.ores.append(Ore("Eclipsicle", "Natura", "Diorite Layer", Tier.ENIGMATIC, rarity_value=53000000))
        self.ores.append(Ore("Polarium", "Natura", "Diorite Layer", Tier.ENIGMATIC, rarity_value=50000005))
        self.ores.append(Ore("Illusory Bubblegram", "Natura", "Diorite Layer", Tier.UNFATHOMABLE, rarity_value=426800050))
        
                                          
        self.ores.append(Ore("Blazuine", "Natura", "Obsidian Layer", Tier.EXOTIC, rarity_value=5700000))
        self.ores.append(Ore("Exolite", "Natura", "Obsidian Layer", Tier.EXOTIC, rarity_value=2432100))
        self.ores.append(Ore("Formidulus", "Natura", "Obsidian Layer", Tier.EXQUISITE, rarity_value=12302022))
        self.ores.append(Ore("Obscuralis", "Natura", "Obsidian Layer", Tier.EXQUISITE, rarity_value=9230230))
        self.ores.append(Ore("Sentient Viscera", "Natura", "Obsidian Layer", Tier.TRANSCENDENT, rarity_value=34500000))
        self.ores.append(Ore("Speatrium", "Natura", "Obsidian Layer", Tier.TRANSCENDENT, rarity_value=29200000))
        self.ores.append(Ore("Inkonium", "Natura", "Obsidian Layer", Tier.ENIGMATIC, rarity_value=62700000))
        self.ores.append(Ore("Ravenmare", "Natura", "Obsidian Layer", Tier.ENIGMATIC, rarity_value=80320000))
        self.ores.append(Ore("Nyctophyte", "Natura", "Obsidian Layer", Tier.UNFATHOMABLE, rarity_value=538000000))
        
                                        
        self.ores.append(Ore("Photoprisma", "Natura", "Marble Layer", Tier.EXOTIC, rarity_value=2300000))
        self.ores.append(Ore("Temporum", "Natura", "Marble Layer", Tier.EXOTIC, rarity_value=5555555))
        self.ores.append(Ore("Ornalium", "Natura", "Marble Layer", Tier.EXQUISITE, rarity_value=9100000))
        self.ores.append(Ore("Aether", "Natura", "Marble Layer", Tier.TRANSCENDENT, rarity_value=22000000))
        self.ores.append(Ore("Luminatite", "Natura", "Marble Layer", Tier.TRANSCENDENT, rarity_value=34350000))
        self.ores.append(Ore("Trinitium", "Natura", "Marble Layer", Tier.TRANSCENDENT, rarity_value=33333333))
        self.ores.append(Ore("Elementium", "Natura", "Marble Layer", Tier.ENIGMATIC, rarity_value=54000000))
        self.ores.append(Ore("Musereign", "Natura", "Marble Layer", Tier.ENIGMATIC, rarity_value=74102000))
        self.ores.append(Ore("Idolium", "Natura", "Marble Layer", Tier.UNFATHOMABLE, rarity_value=170000000))
        
                                        
        self.ores.append(Ore("Poiseon", "Natura", "Mantle Layer", Tier.EXOTIC, rarity_value=3333333))
        self.ores.append(Ore("Polonium", "Natura", "Mantle Layer", Tier.EXOTIC, rarity_value=5555555))
        self.ores.append(Ore("Euclideum", "Natura", "Mantle Layer", Tier.EXQUISITE, rarity_value=14142135))
        self.ores.append(Ore("Vitrilyx", "Natura", "Mantle Layer", Tier.EXQUISITE, rarity_value=9000000))
        self.ores.append(Ore("Albinite", "Natura", "Mantle Layer", Tier.TRANSCENDENT, rarity_value=44444444))
        self.ores.append(Ore("Exoretic", "Natura", "Mantle Layer", Tier.TRANSCENDENT, rarity_value=40000000))
        self.ores.append(Ore("Scarfyte", "Natura", "Mantle Layer", Tier.TRANSCENDENT, rarity_value=25500000))
        self.ores.append(Ore("Glitzar", "Natura", "Mantle Layer", Tier.ENIGMATIC, rarity_value=92000000))
        self.ores.append(Ore("Magnetyx", "Natura", "Mantle Layer", Tier.ENIGMATIC, rarity_value=74500000))
        self.ores.append(Ore("Scribbal", "Natura", "Mantle Layer", Tier.UNFATHOMABLE, rarity_value=200000000))
        
                                                                                                              
        self.ores.append(Ore("Combustal", "Natura", "Outer Core Layer", Tier.EXOTIC, rarity_value=5500000))
        self.ores.append(Ore("Flaeon", "Natura", "Outer Core Layer", Tier.EXOTIC, rarity_value=3333333))
        self.ores.append(Ore("Thundarian", "Natura", "Outer Core Layer", Tier.EXOTIC, rarity_value=2400000))
        self.ores.append(Ore("Bonfire", "Natura", "Outer Core Layer", Tier.EXQUISITE, rarity_value=12000000))
        self.ores.append(Ore("Cleopatrite", "Natura", "Outer Core Layer", Tier.TRANSCENDENT, rarity_value=22500000))
        self.ores.append(Ore("Suncindium", "Natura", "Outer Core Layer", Tier.TRANSCENDENT, rarity_value=20500000))
        self.ores.append(Ore("Xynarium", "Natura", "Outer Core Layer", Tier.TRANSCENDENT, rarity_value=28000000))
        self.ores.append(Ore("Dyronsinite", "Natura", "Outer Core Layer", Tier.ENIGMATIC, rarity_value=63000000))
        self.ores.append(Ore("Gargantium", "Natura", "Outer Core Layer", Tier.ENIGMATIC, rarity_value=71300000))
        self.ores.append(Ore("Dynamo of Fate", "Natura", "Outer Core Layer", Tier.UNFATHOMABLE, rarity_value=750000000))
        
                                            
        self.ores.append(Ore("Accretium", "Natura", "Inner Core Layer", Tier.EXOTIC, rarity_value=3820000))
        self.ores.append(Ore("Combustal", "Natura", "Inner Core Layer", Tier.EXOTIC, rarity_value=5500000))
        self.ores.append(Ore("Flaeon", "Natura", "Inner Core Layer", Tier.EXOTIC, rarity_value=3333333))
        self.ores.append(Ore("Emberstyx", "Natura", "Inner Core Layer", Tier.EXQUISITE, rarity_value=14000000))
        self.ores.append(Ore("Cleopatrite", "Natura", "Inner Core Layer", Tier.TRANSCENDENT, rarity_value=22500000))
        self.ores.append(Ore("Vulkavium", "Natura", "Inner Core Layer", Tier.TRANSCENDENT, rarity_value=23100000))
        self.ores.append(Ore("Xynarium", "Natura", "Inner Core Layer", Tier.TRANSCENDENT, rarity_value=28000000))
        self.ores.append(Ore("Elbrus' Pride", "Natura", "Inner Core Layer", Tier.ENIGMATIC, rarity_value=82000000))
        self.ores.append(Ore("Ω", "Natura", "Inner Core Layer", Tier.ENIGMATIC, rarity_value=75000000))
        self.ores.append(Ore("Chrysalis", "Natura", "Inner Core Layer", Tier.OTHERWORLDLY, rarity_value=800000000))

                                                           
        self.ores.append(Ore("Zanarchium", "Natura", "World Exclusive", Tier.ZENITH, rarity_value=68750000))
        
                                    
                     
        self.ores.append(Ore("Cerlustrium", "Natura", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=25600000, is_cave_exclusive=True, cave_type="Frozen"))
                       
        self.ores.append(Ore("Teslarium", "Natura", "Cave Exclusive", Tier.EXOTIC, rarity_value=350000, is_cave_exclusive=True, cave_type="Metallic"))
                    
        self.ores.append(Ore("Drusentyl", "Natura", "Cave Exclusive", Tier.EXQUISITE, rarity_value=1100000, is_cave_exclusive=True, cave_type="Geode"))
        self.ores.append(Ore("Empress of Light", "Natura", "Cave Exclusive", Tier.UNFATHOMABLE, rarity_value=8000000, is_cave_exclusive=True, cave_type="Geode"))
                        
        self.ores.append(Ore("Hallowed Prism", "Natura", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=2240000, is_cave_exclusive=True, cave_type="Elemental"))
                     
        self.ores.append(Ore("Machina", "Natura", "Cave Exclusive", Tier.OTHERWORLDLY, rarity_value=37700000, is_cave_exclusive=True, cave_type="Divine"))
                        
        self.ores.append(Ore("π", "Natura", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=3141592, is_cave_exclusive=True, cave_type="Prismatic"))
                   
        self.ores.append(Ore("Void Reaver", "Natura", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=3210000, is_cave_exclusive=True, cave_type="Void"))
                              
        self.ores.append(Ore("Ophanim", "Natura", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=377777, is_cave_exclusive=True, cave_type="Gilded"))
        
                        
                                       
        self.ores.append(Ore("Matterium", "Caverna", "Slate Layer", Tier.EXOTIC, rarity_value=3125000))
        self.ores.append(Ore("Atomium", "Caverna", "Slate Layer", Tier.EXQUISITE, rarity_value=9091929))
        self.ores.append(Ore("Cognicite", "Caverna", "Slate Layer", Tier.EXQUISITE, rarity_value=14000000))
        self.ores.append(Ore("Plasmonium", "Caverna", "Slate Layer", Tier.TRANSCENDENT, rarity_value=24000000))
        self.ores.append(Ore("Stazenium", "Caverna", "Slate Layer", Tier.TRANSCENDENT, rarity_value=39550000))
        self.ores.append(Ore("Continuum Rift", "Caverna", "Slate Layer", Tier.ENIGMATIC, rarity_value=66200000))
        self.ores.append(Ore("Terminus", "Caverna", "Slate Layer", Tier.ENIGMATIC, rarity_value=73150000))
        self.ores.append(Ore("The Cylinder", "Caverna", "Slate Layer", Tier.UNFATHOMABLE, rarity_value=201061929))
        
                                            
        self.ores.append(Ore("Covellite", "Caverna", "Permafrost Layer", Tier.EXOTIC, rarity_value=4400400))
        self.ores.append(Ore("Hexagelite", "Caverna", "Permafrost Layer", Tier.EXQUISITE, rarity_value=11000000))
        self.ores.append(Ore("Laivertine", "Caverna", "Permafrost Layer", Tier.EXQUISITE, rarity_value=14000000))
        self.ores.append(Ore("Coselnix", "Caverna", "Permafrost Layer", Tier.TRANSCENDENT, rarity_value=22000000))
        self.ores.append(Ore("Heart of the Frosted", "Caverna", "Permafrost Layer", Tier.TRANSCENDENT, rarity_value=37280000))
        self.ores.append(Ore("Placongela", "Caverna", "Permafrost Layer", Tier.ENIGMATIC, rarity_value=79408000))
        self.ores.append(Ore("Frostrainium", "Caverna", "Permafrost Layer", Tier.ENIGMATIC, rarity_value=87290000))
        self.ores.append(Ore("Caelarius", "Caverna", "Permafrost Layer", Tier.UNFATHOMABLE, rarity_value=583000000))
        
                                              
        self.ores.append(Ore("Accretite", "Caverna", "Shatterstone Layer", Tier.EXOTIC, rarity_value=6500000))
        self.ores.append(Ore("Entiniol", "Caverna", "Shatterstone Layer", Tier.EXOTIC, rarity_value=7020000))
        self.ores.append(Ore("Optimivium", "Caverna", "Shatterstone Layer", Tier.EXQUISITE, rarity_value=9280090))
        self.ores.append(Ore("Catastormite", "Caverna", "Shatterstone Layer", Tier.TRANSCENDENT, rarity_value=28600000))
        self.ores.append(Ore("Contravexium", "Caverna", "Shatterstone Layer", Tier.TRANSCENDENT, rarity_value=39500000))
        self.ores.append(Ore("Neomandelite", "Caverna", "Shatterstone Layer", Tier.ENIGMATIC, rarity_value=68100490))
        self.ores.append(Ore("Vitriol", "Caverna", "Shatterstone Layer", Tier.ENIGMATIC, rarity_value=94000280))
        self.ores.append(Ore("Acrimony", "Caverna", "Shatterstone Layer", Tier.UNFATHOMABLE, rarity_value=257280000))
        
                                          
        self.ores.append(Ore("Crystal Oculite", "Caverna", "Riftrock Layer", Tier.EXOTIC, rarity_value=3478290))
        self.ores.append(Ore("Enchantium", "Caverna", "Riftrock Layer", Tier.EXOTIC, rarity_value=7138000))
        self.ores.append(Ore("Torilite", "Caverna", "Riftrock Layer", Tier.EXQUISITE, rarity_value=11250000))
        self.ores.append(Ore("Spiritian", "Caverna", "Riftrock Layer", Tier.TRANSCENDENT, rarity_value=24800000))
        self.ores.append(Ore("Twilight Mist", "Caverna", "Riftrock Layer", Tier.TRANSCENDENT, rarity_value=28580045))
        self.ores.append(Ore("Unsteady Filaments", "Caverna", "Riftrock Layer", Tier.TRANSCENDENT, rarity_value=33480000))
        self.ores.append(Ore("Celestivian", "Caverna", "Riftrock Layer", Tier.ENIGMATIC, rarity_value=56000000))
        self.ores.append(Ore("Unearthly Cubes", "Caverna", "Riftrock Layer", Tier.ENIGMATIC, rarity_value=64778939))
        self.ores.append(Ore("NOO P α", "Caverna", "Riftrock Layer", Tier.UNFATHOMABLE, rarity_value=709000750))
        
                                            
        self.ores.append(Ore("Arcaleus", "Caverna", "Darkmatter Layer", Tier.EXOTIC, rarity_value=6180980))
        self.ores.append(Ore("Aurantial", "Caverna", "Darkmatter Layer", Tier.EXOTIC, rarity_value=4411920))
        self.ores.append(Ore("Circeterra", "Caverna", "Darkmatter Layer", Tier.EXQUISITE, rarity_value=12500000))
        self.ores.append(Ore("Cosmic Treasure", "Caverna", "Darkmatter Layer", Tier.EXQUISITE, rarity_value=8000800))
        self.ores.append(Ore("Galactic Rupture", "Caverna", "Darkmatter Layer", Tier.TRANSCENDENT, rarity_value=24480000))
        self.ores.append(Ore("Icarus", "Caverna", "Darkmatter Layer", Tier.TRANSCENDENT, rarity_value=38190000))
        self.ores.append(Ore("Rigel", "Caverna", "Darkmatter Layer", Tier.TRANSCENDENT, rarity_value=20565000))
        self.ores.append(Ore("Coronal Flare", "Caverna", "Darkmatter Layer", Tier.ENIGMATIC, rarity_value=65000000))
        self.ores.append(Ore("Gravitaticor", "Caverna", "Darkmatter Layer", Tier.ENIGMATIC, rarity_value=71120000))
        self.ores.append(Ore("Quasar 618", "Caverna", "Darkmatter Layer", Tier.UNFATHOMABLE, rarity_value=618000000))
        
                                      
        self.ores.append(Ore("Phobetor", "Caverna", "Void Layer", Tier.EXOTIC, rarity_value=3890000))
        self.ores.append(Ore("Voidflower", "Caverna", "Void Layer", Tier.EXOTIC, rarity_value=5826000))
        self.ores.append(Ore("Estrela", "Caverna", "Void Layer", Tier.EXQUISITE, rarity_value=13200000))
        self.ores.append(Ore("Kaleidium", "Caverna", "Void Layer", Tier.EXQUISITE, rarity_value=7878000))
        self.ores.append(Ore("Andromidium", "Caverna", "Void Layer", Tier.TRANSCENDENT, rarity_value=21780000))
        self.ores.append(Ore("Magicis Floreat", "Caverna", "Void Layer", Tier.TRANSCENDENT, rarity_value=28123000))
        self.ores.append(Ore("NOO S-Sing. Tl", "Caverna", "Void Layer", Tier.TRANSCENDENT, rarity_value=38449000))
        self.ores.append(Ore("Obliveracy Endmost", "Caverna", "Void Layer", Tier.ENIGMATIC, rarity_value=77061652))
        self.ores.append(Ore("Voyanesia", "Caverna", "Void Layer", Tier.ENIGMATIC, rarity_value=53721739))
        self.ores.append(Ore("Sirius-X10", "Caverna", "Void Layer", Tier.UNFATHOMABLE, rarity_value=446153846))
        self.ores.append(Ore("Retina", "Caverna", "Void Layer", Tier.OTHERWORLDLY, rarity_value=734769915))
        
                                     
                       
        self.ores.append(Ore("Exdeus", "Caverna", "Cave Exclusive", Tier.UNFATHOMABLE, rarity_value=32372000, is_cave_exclusive=True, cave_type="Unstable"))
                       
        self.ores.append(Ore("Cygnus", "Caverna", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=10480900, is_cave_exclusive=True, cave_type="Galactic"))
                        
        self.ores.append(Ore("Asterium", "Caverna", "Cave Exclusive", Tier.EXOTIC, rarity_value=361000, is_cave_exclusive=True, cave_type="Enchanted"))
        self.ores.append(Ore("Observatorium", "Caverna", "Cave Exclusive", Tier.OTHERWORLDLY, rarity_value=63245790, is_cave_exclusive=True, cave_type="Enchanted"))
                       
        self.ores.append(Ore("Lavortia", "Caverna", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=1347290, is_cave_exclusive=True, cave_type="Luminous"))
                        
        self.ores.append(Ore("Lunarian", "Caverna", "Cave Exclusive", Tier.EXQUISITE, rarity_value=411000, is_cave_exclusive=True, cave_type="Nightfall"))
                               
        self.ores.append(Ore("Hyperheated Quasar", "Caverna", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=810000, is_cave_exclusive=True, cave_type="Gilded"))
        
                       
                                            
        self.ores.append(Ore("Auriceph", "Digita", "Statistone Layer", Tier.EXOTIC, rarity_value=7500000))
        self.ores.append(Ore("Decimora", "Digita", "Statistone Layer", Tier.EXOTIC, rarity_value=2302100))
        self.ores.append(Ore("Ethyrilem", "Digita", "Statistone Layer", Tier.EXQUISITE, rarity_value=12777777))
        self.ores.append(Ore("Fluxorium", "Digita", "Statistone Layer", Tier.EXQUISITE, rarity_value=10010023))
        self.ores.append(Ore("Plasverlite", "Digita", "Statistone Layer", Tier.TRANSCENDENT, rarity_value=40000200))
        self.ores.append(Ore("Teslarian", "Digita", "Statistone Layer", Tier.TRANSCENDENT, rarity_value=25239392))
        self.ores.append(Ore("Voltiflux", "Digita", "Statistone Layer", Tier.TRANSCENDENT, rarity_value=35000200))
        self.ores.append(Ore("Phastuanyx", "Digita", "Statistone Layer", Tier.ENIGMATIC, rarity_value=61200216))
        self.ores.append(Ore("Photon Fluxulite", "Digita", "Statistone Layer", Tier.ENIGMATIC, rarity_value=53120000))
        self.ores.append(Ore("Dyvantium", "Digita", "Statistone Layer", Tier.UNFATHOMABLE, rarity_value=290000000))
        self.ores.append(Ore("GENESIS", "Digita", "Statistone Layer", Tier.UNFATHOMABLE, rarity_value=380000000))
        
                                           
        self.ores.append(Ore("Starbit", "Digita", "Wireframe Layer", Tier.EXOTIC, rarity_value=3120100))
        self.ores.append(Ore("Triginium", "Digita", "Wireframe Layer", Tier.EXOTIC, rarity_value=2100101))
        self.ores.append(Ore("MK2 Sonar", "Digita", "Wireframe Layer", Tier.EXQUISITE, rarity_value=8100102))
        self.ores.append(Ore("W|REFRAME", "Digita", "Wireframe Layer", Tier.EXQUISITE, rarity_value=13112101))
        self.ores.append(Ore("Cosmonolithius", "Digita", "Wireframe Layer", Tier.TRANSCENDENT, rarity_value=45000000))
        self.ores.append(Ore("Terascental", "Digita", "Wireframe Layer", Tier.TRANSCENDENT, rarity_value=26000100))
        self.ores.append(Ore("Aesthetic Reality", "Digita", "Wireframe Layer", Tier.ENIGMATIC, rarity_value=90000000))
        self.ores.append(Ore("Holovirlux", "Digita", "Wireframe Layer", Tier.ENIGMATIC, rarity_value=70320000))
        self.ores.append(Ore("Sustained Axiom", "Digita", "Wireframe Layer", Tier.ENIGMATIC, rarity_value=68200100))
        self.ores.append(Ore("404 Gateway", "Digita", "Wireframe Layer", Tier.UNFATHOMABLE, rarity_value=404404404))
        self.ores.append(Ore("Theon", "Digita", "Wireframe Layer", Tier.UNFATHOMABLE, rarity_value=720000000))
        
                                           
        self.ores.append(Ore("Icosaformite", "Digita", "Matricite Layer", Tier.EXOTIC, rarity_value=4005000))
        self.ores.append(Ore("Matrisse", "Digita", "Matricite Layer", Tier.EXOTIC, rarity_value=6000000))
        self.ores.append(Ore("Limelight", "Digita", "Matricite Layer", Tier.EXQUISITE, rarity_value=9210000))
        self.ores.append(Ore("Revonet", "Digita", "Matricite Layer", Tier.EXQUISITE, rarity_value=13100310))
        self.ores.append(Ore("Virtulily", "Digita", "Matricite Layer", Tier.TRANSCENDENT, rarity_value=22100201))
        self.ores.append(Ore("Δ", "Digita", "Matricite Layer", Tier.TRANSCENDENT, rarity_value=33333333))
        self.ores.append(Ore("M4TR1X", "Digita", "Matricite Layer", Tier.ENIGMATIC, rarity_value=51101101))
        self.ores.append(Ore("Virtuosity", "Digita", "Matricite Layer", Tier.ENIGMATIC, rarity_value=80200100))
        self.ores.append(Ore("Equalizosity", "Digita", "Matricite Layer", Tier.UNFATHOMABLE, rarity_value=300020000))
        self.ores.append(Ore("CHECKPOINT.0901", "Digita", "Matricite Layer", Tier.UNFATHOMABLE, rarity_value=500000000))
        
                                           
        self.ores.append(Ore("Geigite Receptacle", "Digita", "Mechaloid Layer", Tier.EXOTIC, rarity_value=3520230))
        self.ores.append(Ore("Mechaspark", "Digita", "Mechaloid Layer", Tier.EXOTIC, rarity_value=4120101))
        self.ores.append(Ore("Invalid Apprehension", "Digita", "Mechaloid Layer", Tier.EXQUISITE, rarity_value=10000011))
        self.ores.append(Ore("Sardonyx", "Digita", "Mechaloid Layer", Tier.EXQUISITE, rarity_value=13102103))
        self.ores.append(Ore("Chaotica", "Digita", "Mechaloid Layer", Tier.TRANSCENDENT, rarity_value=20000020))
        self.ores.append(Ore("Cryofantasia", "Digita", "Mechaloid Layer", Tier.TRANSCENDENT, rarity_value=24032129))
        self.ores.append(Ore("Spherocube", "Digita", "Mechaloid Layer", Tier.TRANSCENDENT, rarity_value=18000120))
        self.ores.append(Ore("Darkmatter Stabilizer", "Digita", "Mechaloid Layer", Tier.ENIGMATIC, rarity_value=65201293))
        self.ores.append(Ore("Torpensangor", "Digita", "Mechaloid Layer", Tier.ENIGMATIC, rarity_value=54020010))
        self.ores.append(Ore("Vily Narila", "Digita", "Mechaloid Layer", Tier.UNFATHOMABLE, rarity_value=232203032))
        self.ores.append(Ore("Jadefall", "Digita", "Mechaloid Layer", Tier.OTHERWORLDLY, rarity_value=810000000))
        
                                       
        self.ores.append(Ore("Eye of the Siren", "Digita", "Steel Layer", Tier.EXOTIC, rarity_value=5120129))
        self.ores.append(Ore("Terraformation", "Digita", "Steel Layer", Tier.EXOTIC, rarity_value=2456294))
        self.ores.append(Ore("Statigen", "Digita", "Steel Layer", Tier.EXQUISITE, rarity_value=13219000))
        self.ores.append(Ore("Draesdruvite", "Digita", "Steel Layer", Tier.TRANSCENDENT, rarity_value=25109288))
        self.ores.append(Ore("Lifeforce Drainer", "Digita", "Steel Layer", Tier.TRANSCENDENT, rarity_value=23201120))
        self.ores.append(Ore("Pulsō Relicta", "Digita", "Steel Layer", Tier.TRANSCENDENT, rarity_value=36120188))
        self.ores.append(Ore("Apexilec", "Digita", "Steel Layer", Tier.ENIGMATIC, rarity_value=90100990))
        self.ores.append(Ore("Chicago", "Digita", "Steel Layer", Tier.ENIGMATIC, rarity_value=76767767))
        self.ores.append(Ore("Computer Annihilator 4600 MK. II", "Digita", "Steel Layer", Tier.UNFATHOMABLE, rarity_value=150000000))
        self.ores.append(Ore("Mekanos", "Digita", "Steel Layer", Tier.UNFATHOMABLE, rarity_value=635703105))
        
                                           
        self.ores.append(Ore("Paraxenos", "Digita", "Penumbrum Layer", Tier.EXOTIC, rarity_value=2600000))
        self.ores.append(Ore("Tetrium", "Digita", "Penumbrum Layer", Tier.EXOTIC, rarity_value=4321012))
        self.ores.append(Ore("Chromatechnimar", "Digita", "Penumbrum Layer", Tier.EXQUISITE, rarity_value=7600000))
        self.ores.append(Ore("Printorbs", "Digita", "Penumbrum Layer", Tier.EXQUISITE, rarity_value=13201919))
        self.ores.append(Ore("Pixelated Mass", "Digita", "Penumbrum Layer", Tier.TRANSCENDENT, rarity_value=39219101))
        self.ores.append(Ore("Speedulant", "Digita", "Penumbrum Layer", Tier.TRANSCENDENT, rarity_value=26100106))
        self.ores.append(Ore("Novurbite", "Digita", "Penumbrum Layer", Tier.ENIGMATIC, rarity_value=58200100))
        self.ores.append(Ore("Polaroidium", "Digita", "Penumbrum Layer", Tier.ENIGMATIC, rarity_value=94444444))
        self.ores.append(Ore("Vertiglow", "Digita", "Penumbrum Layer", Tier.UNFATHOMABLE, rarity_value=610610610))
        self.ores.append(Ore("VANTABLACK", "Digita", "Penumbrum Layer", Tier.OTHERWORLDLY, rarity_value=2500000000))
        
                                           
        self.ores.append(Ore("Mistirine", "Digita", "Twilement Layer", Tier.EXOTIC, rarity_value=6102399))
        self.ores.append(Ore("Onian", "Digita", "Twilement Layer", Tier.EXOTIC, rarity_value=4101010))
        self.ores.append(Ore("Quantalyx", "Digita", "Twilement Layer", Tier.EXQUISITE, rarity_value=10000000))
        self.ores.append(Ore("Vys", "Digita", "Twilement Layer", Tier.EXQUISITE, rarity_value=13500000))
        self.ores.append(Ore("Portalium", "Digita", "Twilement Layer", Tier.TRANSCENDENT, rarity_value=44320000))
        self.ores.append(Ore("Wisticora", "Digita", "Twilement Layer", Tier.TRANSCENDENT, rarity_value=19199991))
        self.ores.append(Ore("Exopolis", "Digita", "Twilement Layer", Tier.ENIGMATIC, rarity_value=67200099))
        self.ores.append(Ore("Navigate", "Digita", "Twilement Layer", Tier.ENIGMATIC, rarity_value=88888888))
        self.ores.append(Ore("Dreamscape", "Digita", "Twilement Layer", Tier.UNFATHOMABLE, rarity_value=230000000))
        self.ores.append(Ore("COSMIC_SPLIT", "Digita", "Twilement Layer", Tier.OTHERWORLDLY, rarity_value=1250000000))
        
                                           
        self.ores.append(Ore("Bipulsidine", "Digita", "Cosmorock Layer", Tier.EXOTIC, rarity_value=5100203))
        self.ores.append(Ore("Emberis", "Digita", "Cosmorock Layer", Tier.EXOTIC, rarity_value=3000003))
        self.ores.append(Ore("Kenospina", "Digita", "Cosmorock Layer", Tier.EXQUISITE, rarity_value=11000000))
        self.ores.append(Ore("Nebula Nexus", "Digita", "Cosmorock Layer", Tier.EXQUISITE, rarity_value=9999999))
        self.ores.append(Ore("Cosmilite", "Digita", "Cosmorock Layer", Tier.TRANSCENDENT, rarity_value=42100021))
        self.ores.append(Ore("Star-Zero", "Digita", "Cosmorock Layer", Tier.TRANSCENDENT, rarity_value=20000000))
        self.ores.append(Ore("Galaxia", "Digita", "Cosmorock Layer", Tier.ENIGMATIC, rarity_value=65001125))
        self.ores.append(Ore("Nebulova", "Digita", "Cosmorock Layer", Tier.ENIGMATIC, rarity_value=71000000))
        self.ores.append(Ore("Duostella", "Digita", "Cosmorock Layer", Tier.UNFATHOMABLE, rarity_value=333333333))
        self.ores.append(Ore("Monolith of Origin", "Digita", "Cosmorock Layer", Tier.UNFATHOMABLE, rarity_value=515555595))
        
                                        
        self.ores.append(Ore("Bug", "Digita", "Glitch Layer", Tier.EXOTIC, rarity_value=4004120))
        self.ores.append(Ore("Poor Connection", "Digita", "Glitch Layer", Tier.EXOTIC, rarity_value=5129100))
        self.ores.append(Ore("Cyberillic", "Digita", "Glitch Layer", Tier.EXQUISITE, rarity_value=14001014))
        self.ores.append(Ore("Gravitron", "Digita", "Glitch Layer", Tier.EXQUISITE, rarity_value=8001291))
        self.ores.append(Ore("CORRUPTELA", "Digita", "Glitch Layer", Tier.TRANSCENDENT, rarity_value=26910012))
        self.ores.append(Ore("Matrixalga", "Digita", "Glitch Layer", Tier.TRANSCENDENT, rarity_value=30001000))
        self.ores.append(Ore("Hyperfullerene", "Digita", "Glitch Layer", Tier.ENIGMATIC, rarity_value=85000058))
        self.ores.append(Ore("Monocritica", "Digita", "Glitch Layer", Tier.ENIGMATIC, rarity_value=72001000))
        self.ores.append(Ore("Achromatopsia", "Digita", "Glitch Layer", Tier.UNFATHOMABLE, rarity_value=198999999))
        self.ores.append(Ore("Unstable Megacore", "Digita", "Glitch Layer", Tier.OTHERWORLDLY, rarity_value=3500000000))
        
                                       
        self.ores.append(Ore("Corruptal", "Digita", "Virus Layer", Tier.EXOTIC, rarity_value=6192174))
        self.ores.append(Ore("Glitchreax", "Digita", "Virus Layer", Tier.EXOTIC, rarity_value=4192188))
        self.ores.append(Ore("C-ORE ERROR", "Digita", "Virus Layer", Tier.EXQUISITE, rarity_value=9699991))
        self.ores.append(Ore("Oscilline", "Digita", "Virus Layer", Tier.EXQUISITE, rarity_value=12100991))
        self.ores.append(Ore("Hiderae", "Digita", "Virus Layer", Tier.TRANSCENDENT, rarity_value=27100100))
        self.ores.append(Ore("Luridium", "Digita", "Virus Layer", Tier.TRANSCENDENT, rarity_value=47001400))
        self.ores.append(Ore("Mendelevium", "Digita", "Virus Layer", Tier.TRANSCENDENT, rarity_value=38000888))
        self.ores.append(Ore("32-Bit Integer Limit", "Digita", "Virus Layer", Tier.ENIGMATIC, rarity_value=67108864))
        self.ores.append(Ore("Techtrilyx", "Digita", "Virus Layer", Tier.ENIGMATIC, rarity_value=71117771))
        self.ores.append(Ore("The Firewall", "Digita", "Virus Layer", Tier.ENIGMATIC, rarity_value=93000000))
        self.ores.append(Ore("TROJ4N", "Digita", "Virus Layer", Tier.UNFATHOMABLE, rarity_value=589320394))
        self.ores.append(Ore("SCARLET", "Digita", "Virus Layer", Tier.OTHERWORLDLY, rarity_value=910837416))
        
                                    
                              
        self.ores.append(Ore("Solace", "Digita", "Cave Exclusive", Tier.UNFATHOMABLE, rarity_value=2332960, is_cave_exclusive=True, cave_type="Gilded"))
                     
        self.ores.append(Ore("Heliotropic Fracture", "Digita", "Cave Exclusive", Tier.EXOTIC, rarity_value=550000, is_cave_exclusive=True, cave_type="Starry"))
        self.ores.append(Ore("Spaceshatter", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=1700000, is_cave_exclusive=True, cave_type="Starry"))
        self.ores.append(Ore("Nebula Tempest", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=3000000, is_cave_exclusive=True, cave_type="Starry"))
        self.ores.append(Ore("Lumenyl", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=4250000, is_cave_exclusive=True, cave_type="Starry"))
        self.ores.append(Ore("Astraea", "Digita", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=11000000, is_cave_exclusive=True, cave_type="Starry"))
        self.ores.append(Ore("Aetherion", "Digita", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=23644444, is_cave_exclusive=True, cave_type="Starry"))
        self.ores.append(Ore("Syderea", "Digita", "Cave Exclusive", Tier.OTHERWORLDLY, rarity_value=110000000, is_cave_exclusive=True, cave_type="Starry"))
                     
        self.ores.append(Ore("Synthetyl", "Digita", "Cave Exclusive", Tier.EXOTIC, rarity_value=500000, is_cave_exclusive=True, cave_type="Matrix"))
        self.ores.append(Ore("4FA208", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=992907, is_cave_exclusive=True, cave_type="Matrix"))
        self.ores.append(Ore("F24D43", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=992907, is_cave_exclusive=True, cave_type="Matrix"))
        self.ores.append(Ore("Geometric Quadrant", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=4255319, is_cave_exclusive=True, cave_type="Matrix"))
        self.ores.append(Ore("Geometrix", "Digita", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=9219858, is_cave_exclusive=True, cave_type="Matrix"))
        self.ores.append(Ore("Low.HP", "Digita", "Cave Exclusive", Tier.UNFATHOMABLE, rarity_value=20567375, is_cave_exclusive=True, cave_type="Matrix"))
                      
        self.ores.append(Ore("Electricore", "Digita", "Cave Exclusive", Tier.EXOTIC, rarity_value=248254, is_cave_exclusive=True, cave_type="Voltaic"))
        self.ores.append(Ore("Pariluxem", "Digita", "Cave Exclusive", Tier.EXOTIC, rarity_value=331414, is_cave_exclusive=True, cave_type="Voltaic"))
        self.ores.append(Ore("Corruptryx", "Digita", "Cave Exclusive", Tier.EXOTIC, rarity_value=468000, is_cave_exclusive=True, cave_type="Voltaic"))
        self.ores.append(Ore("Valenarium", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=769336, is_cave_exclusive=True, cave_type="Voltaic"))
        self.ores.append(Ore("Luminosaic", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=2816020, is_cave_exclusive=True, cave_type="Voltaic"))
        self.ores.append(Ore("Roundabout", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=3754693, is_cave_exclusive=True, cave_type="Voltaic"))
        self.ores.append(Ore("generic68-B", "Digita", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=9386733, is_cave_exclusive=True, cave_type="Voltaic"))
        self.ores.append(Ore("Antlerion", "Digita", "Cave Exclusive", Tier.UNFATHOMABLE, rarity_value=19086357, is_cave_exclusive=True, cave_type="Voltaic"))
                          
        self.ores.append(Ore("Varonela", "Digita", "Cave Exclusive", Tier.EXOTIC, rarity_value=180000, is_cave_exclusive=True, cave_type="Bichromatic"))
        self.ores.append(Ore("Arcanicium", "Digita", "Cave Exclusive", Tier.EXOTIC, rarity_value=246646, is_cave_exclusive=True, cave_type="Bichromatic"))
        self.ores.append(Ore("Altair", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=506595, is_cave_exclusive=True, cave_type="Bichromatic"))
        self.ores.append(Ore("@Combustl0n_+_Syst3m", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=1013171, is_cave_exclusive=True, cave_type="Bichromatic"))
        self.ores.append(Ore("Fatennial", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=2608915, is_cave_exclusive=True, cave_type="Bichromatic"))
        self.ores.append(Ore("Amaranthine", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=3310000, is_cave_exclusive=True, cave_type="Bichromatic"))
        self.ores.append(Ore("Sword Waltz", "Digita", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=5628729, is_cave_exclusive=True, cave_type="Bichromatic"))
        self.ores.append(Ore("Thermazine", "Digita", "Cave Exclusive", Tier.UNFATHOMABLE, rarity_value=19250253, is_cave_exclusive=True, cave_type="Bichromatic"))
                            
        self.ores.append(Ore("Anulus", "Digita", "Cave Exclusive", Tier.EXOTIC, rarity_value=200000, is_cave_exclusive=True, cave_type="Monoprismatic"))
        self.ores.append(Ore("Hypnosia", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=400000, is_cave_exclusive=True, cave_type="Monoprismatic"))
        self.ores.append(Ore("Iridistar", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=600000, is_cave_exclusive=True, cave_type="Monoprismatic"))
        self.ores.append(Ore("Finalitium", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=1100000, is_cave_exclusive=True, cave_type="Monoprismatic"))
        self.ores.append(Ore("Canivesium", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=1800000, is_cave_exclusive=True, cave_type="Monoprismatic"))
        self.ores.append(Ore("Illusorium", "Digita", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=3000000, is_cave_exclusive=True, cave_type="Monoprismatic"))
        self.ores.append(Ore("Collapse", "Digita", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=5000000, is_cave_exclusive=True, cave_type="Monoprismatic"))
        self.ores.append(Ore("Universal Collapse", "Digita", "Cave Exclusive", Tier.OTHERWORLDLY, rarity_value=111000000, is_cave_exclusive=True, cave_type="Monoprismatic"))
                      
        self.ores.append(Ore("Magnatoxin", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=369385, is_cave_exclusive=True, cave_type="Malware"))
        self.ores.append(Ore("Fulmara", "Digita", "Cave Exclusive", Tier.EXQUISITE, rarity_value=573262, is_cave_exclusive=True, cave_type="Malware"))
        self.ores.append(Ore("Archaem", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=1477541, is_cave_exclusive=True, cave_type="Malware"))
        self.ores.append(Ore("Malicioutrite", "Digita", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=1912312, is_cave_exclusive=True, cave_type="Malware"))
        self.ores.append(Ore("Monojit", "Digita", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=2955082, is_cave_exclusive=True, cave_type="Malware"))
        self.ores.append(Ore("Cataclysmium", "Digita", "Cave Exclusive", Tier.UNFATHOMABLE, rarity_value=12115839, is_cave_exclusive=True, cave_type="Malware"))
        
                            
                                            
        self.ores.append(Ore("Inktite", "Luna Refuge", "Moon Stone Layer", Tier.EXOTIC, rarity_value=2250000))
        self.ores.append(Ore("Lunar Codex", "Luna Refuge", "Moon Stone Layer", Tier.EXOTIC, rarity_value=6500000))
        self.ores.append(Ore("Lunar Freon", "Luna Refuge", "Moon Stone Layer", Tier.EXOTIC, rarity_value=3333333))
        self.ores.append(Ore("Lunar Aurora", "Luna Refuge", "Moon Stone Layer", Tier.TRANSCENDENT, rarity_value=47000000))
        self.ores.append(Ore("Lunar Neomandelite", "Luna Refuge", "Moon Stone Layer", Tier.TRANSCENDENT, rarity_value=25450000))
        self.ores.append(Ore("Soundstrocity", "Luna Refuge", "Moon Stone Layer", Tier.TRANSCENDENT, rarity_value=31000000))
        self.ores.append(Ore("Flare of Transcendence", "Luna Refuge", "Moon Stone Layer", Tier.ENIGMATIC, rarity_value=63000000))
        self.ores.append(Ore("Lunar Vitriol", "Luna Refuge", "Moon Stone Layer", Tier.ENIGMATIC, rarity_value=63800000))
        self.ores.append(Ore("Lunar Voidirinite", "Luna Refuge", "Moon Stone Layer", Tier.UNFATHOMABLE, rarity_value=750000000))
        
                                             
        self.ores.append(Ore("Lunar Flaeon", "Luna Refuge", "Moon Mantle Layer", Tier.EXOTIC, rarity_value=3333333))
        self.ores.append(Ore("Lutetium", "Luna Refuge", "Moon Mantle Layer", Tier.EXOTIC, rarity_value=2517497))
        self.ores.append(Ore("Electrolyx", "Luna Refuge", "Moon Mantle Layer", Tier.EXQUISITE, rarity_value=15000000))
        self.ores.append(Ore("Protoflare", "Luna Refuge", "Moon Mantle Layer", Tier.EXQUISITE, rarity_value=6000000))
        self.ores.append(Ore("Sagittarius Quasar", "Luna Refuge", "Moon Mantle Layer", Tier.EXQUISITE, rarity_value=8200000))
        self.ores.append(Ore("Illuminyx", "Luna Refuge", "Moon Mantle Layer", Tier.TRANSCENDENT, rarity_value=36000000))
        self.ores.append(Ore("Lunar Trinitium", "Luna Refuge", "Moon Mantle Layer", Tier.TRANSCENDENT, rarity_value=33333333))
        self.ores.append(Ore("Lunar Ω", "Luna Refuge", "Moon Mantle Layer", Tier.ENIGMATIC, rarity_value=50000000))
        self.ores.append(Ore("RGB Pulsar", "Luna Refuge", "Moon Mantle Layer", Tier.ENIGMATIC, rarity_value=70000000))
        self.ores.append(Ore("Surrenial", "Luna Refuge", "Moon Mantle Layer", Tier.ENIGMATIC, rarity_value=52500000))
        self.ores.append(Ore("Armageddium", "Luna Refuge", "Moon Mantle Layer", Tier.UNFATHOMABLE, rarity_value=375000000))
        
                                           
        self.ores.append(Ore("Lunar Halcyon Emission", "Luna Refuge", "Moon Core Layer", Tier.EXOTIC, rarity_value=3400000))
        self.ores.append(Ore("Lunar Poiseon", "Luna Refuge", "Moon Core Layer", Tier.EXOTIC, rarity_value=3333333))
        self.ores.append(Ore("Lunar Astatine", "Luna Refuge", "Moon Core Layer", Tier.EXQUISITE, rarity_value=14000000))
        self.ores.append(Ore("Lunar Malachite", "Luna Refuge", "Moon Core Layer", Tier.EXQUISITE, rarity_value=11500000))
        self.ores.append(Ore("Orb of Discontent", "Luna Refuge", "Moon Core Layer", Tier.TRANSCENDENT, rarity_value=25000000))
        self.ores.append(Ore("Σ", "Luna Refuge", "Moon Core Layer", Tier.TRANSCENDENT, rarity_value=40000000))
        self.ores.append(Ore("Vaporwave Pulsar", "Luna Refuge", "Moon Core Layer", Tier.TRANSCENDENT, rarity_value=19500000))
        self.ores.append(Ore("Lunar Aether", "Luna Refuge", "Moon Core Layer", Tier.ENIGMATIC, rarity_value=58000000))
        self.ores.append(Ore("Lunar Quasar V", "Luna Refuge", "Moon Core Layer", Tier.ENIGMATIC, rarity_value=52340000))
        self.ores.append(Ore("Lunar Quasar 618", "Luna Refuge", "Moon Core Layer", Tier.UNFATHOMABLE, rarity_value=618000000))
        self.ores.append(Ore("Epinephrine", "Luna Refuge", "Moon Core Layer", Tier.OTHERWORLDLY, rarity_value=999999999))
        
                                      
        self.ores.append(Ore("BANANORE", "Luna Refuge", "Rocc Layer", Tier.EXOTIC, rarity_value=6000000))
        self.ores.append(Ore("WATERMELON ORE", "Luna Refuge", "Rocc Layer", Tier.EXOTIC, rarity_value=4500000))
        self.ores.append(Ore("COCONUT ORE", "Luna Refuge", "Rocc Layer", Tier.EXQUISITE, rarity_value=8000000))
        self.ores.append(Ore("CHICKEN Crystal", "Luna Refuge", "Rocc Layer", Tier.TRANSCENDENT, rarity_value=30000000))
        self.ores.append(Ore("the funny", "Luna Refuge", "Rocc Layer", Tier.TRANSCENDENT, rarity_value=40000000))
        self.ores.append(Ore("the unfunny", "Luna Refuge", "Rocc Layer", Tier.TRANSCENDENT, rarity_value=20000000))
        self.ores.append(Ore("garlic bread crystal", "Luna Refuge", "Rocc Layer", Tier.ENIGMATIC, rarity_value=54500000))
        self.ores.append(Ore("SHOWER CRYSTAL", "Luna Refuge", "Rocc Layer", Tier.ENIGMATIC, rarity_value=51500000))
        self.ores.append(Ore("a flare v2", "Luna Refuge", "Rocc Layer", Tier.UNFATHOMABLE, rarity_value=160000000))
        self.ores.append(Ore("Corroplat Pulsar", "Luna Refuge", "Rocc Layer", Tier.UNFATHOMABLE, rarity_value=444444444))
        
                                         
                       
        self.ores.append(Ore("Ascended Flare", "Luna Refuge", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=6000000, is_cave_exclusive=True, cave_type="Magmatic"))
        self.ores.append(Ore("Lunar Gargantium", "Luna Refuge", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=6500000, is_cave_exclusive=True, cave_type="Magmatic"))
        self.ores.append(Ore("Lunar Coronal Flare", "Luna Refuge", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=13150000, is_cave_exclusive=True, cave_type="Magmatic"))
                          
        self.ores.append(Ore("Lunar Coronium", "Luna Refuge", "Cave Exclusive", Tier.EXOTIC, rarity_value=600000, is_cave_exclusive=True, cave_type="Radioactive"))
        self.ores.append(Ore("Lunar Neptunium", "Luna Refuge", "Cave Exclusive", Tier.EXOTIC, rarity_value=800000, is_cave_exclusive=True, cave_type="Radioactive"))
        self.ores.append(Ore("Surgium", "Luna Refuge", "Cave Exclusive", Tier.EXQUISITE, rarity_value=975000, is_cave_exclusive=True, cave_type="Radioactive"))
        self.ores.append(Ore("Lunar Lawrencium", "Luna Refuge", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=6000000, is_cave_exclusive=True, cave_type="Radioactive"))
        self.ores.append(Ore("Oganesson", "Luna Refuge", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=12400000, is_cave_exclusive=True, cave_type="Radioactive"))
                           
        self.ores.append(Ore("Lunar Pulsar Crystal", "Luna Refuge", "Cave Exclusive", Tier.EXOTIC, rarity_value=850000, is_cave_exclusive=True, cave_type="Interstellar"))
        self.ores.append(Ore("Lunar Andromidium", "Luna Refuge", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=3000000, is_cave_exclusive=True, cave_type="Interstellar"))
        self.ores.append(Ore("R136a1", "Luna Refuge", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=5300000, is_cave_exclusive=True, cave_type="Interstellar"))
        self.ores.append(Ore("Lunar HR 5171 A", "Luna Refuge", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=9000000, is_cave_exclusive=True, cave_type="Interstellar"))
        self.ores.append(Ore("HD 160529", "Luna Refuge", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=16000000, is_cave_exclusive=True, cave_type="Interstellar"))
        self.ores.append(Ore("Laniakea Supercluster", "Luna Refuge", "Cave Exclusive", Tier.UNFATHOMABLE, rarity_value=50000000, is_cave_exclusive=True, cave_type="Interstellar"))
                  
        self.ores.append(Ore("Accesinite", "Luna Refuge", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=3000000, is_cave_exclusive=True, cave_type="nil"))
        self.ores.append(Ore("Genuinium", "Luna Refuge", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=3200000, is_cave_exclusive=True, cave_type="nil"))
        self.ores.append(Ore("Fire Crystal", "Luna Refuge", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=3300000, is_cave_exclusive=True, cave_type="nil"))
        self.ores.append(Ore("Pandorite", "Luna Refuge", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=3400000, is_cave_exclusive=True, cave_type="nil"))
        self.ores.append(Ore("NILNAL", "Luna Refuge", "Cave Exclusive", Tier.OTHERWORLDLY, rarity_value=40000000, is_cave_exclusive=True, cave_type="nil"))
                                   
        self.ores.append(Ore("Ambrosia", "Luna Refuge", "Cave Exclusive", Tier.EXQUISITE, rarity_value=11112, is_cave_exclusive=True, cave_type="Gilded"))
        
                         
                                            
        self.ores.append(Ore("Agoraphore", "Aesteria", "Spookstone Layer", Tier.EXOTIC, rarity_value=6230001))
        self.ores.append(Ore("Demonizine", "Aesteria", "Spookstone Layer", Tier.EXOTIC, rarity_value=3600000))
        self.ores.append(Ore("Confined Cataclysm", "Aesteria", "Spookstone Layer", Tier.EXQUISITE, rarity_value=12200200))
        self.ores.append(Ore("Plasmitan", "Aesteria", "Spookstone Layer", Tier.TRANSCENDENT, rarity_value=24800000))
        self.ores.append(Ore("Panselinos", "Aesteria", "Spookstone Layer", Tier.TRANSCENDENT, rarity_value=30140000))
        self.ores.append(Ore("Puppet Master", "Aesteria", "Spookstone Layer", Tier.TRANSCENDENT, rarity_value=37845000))
        self.ores.append(Ore("Phantomalgamation", "Aesteria", "Spookstone Layer", Tier.ENIGMATIC, rarity_value=77600000))
        self.ores.append(Ore("Thalassus", "Aesteria", "Spookstone Layer", Tier.ENIGMATIC, rarity_value=58200000))
        self.ores.append(Ore("Scourge", "Aesteria", "Spookstone Layer", Tier.UNFATHOMABLE, rarity_value=175430000))
        
                                          
        self.ores.append(Ore("Lilaverine", "Aesteria", "Affement Layer", Tier.EXOTIC, rarity_value=2300000))
        self.ores.append(Ore("Rosarium", "Aesteria", "Affement Layer", Tier.EXOTIC, rarity_value=5555555))
        self.ores.append(Ore("Mythical Hive", "Aesteria", "Affement Layer", Tier.EXQUISITE, rarity_value=12121212))
        self.ores.append(Ore("Valentinyl", "Aesteria", "Affement Layer", Tier.EXQUISITE, rarity_value=12222222))
        self.ores.append(Ore("Lovessence", "Aesteria", "Affement Layer", Tier.TRANSCENDENT, rarity_value=22222222))
        self.ores.append(Ore("Sentimentium", "Aesteria", "Affement Layer", Tier.TRANSCENDENT, rarity_value=31300000))
        self.ores.append(Ore("Albuca Spiralis", "Aesteria", "Affement Layer", Tier.ENIGMATIC, rarity_value=70100000))
        self.ores.append(Ore("Amare", "Aesteria", "Affement Layer", Tier.ENIGMATIC, rarity_value=52300000))
        self.ores.append(Ore("Aphrodite's Ring", "Aesteria", "Affement Layer", Tier.UNFATHOMABLE, rarity_value=214000496))
        
                                               
        self.ores.append(Ore("Clotivein", "Aesteria", "Withered Sand Layer", Tier.EXOTIC, rarity_value=7191000))
        self.ores.append(Ore("Silence", "Aesteria", "Withered Sand Layer", Tier.EXOTIC, rarity_value=3260100))
        self.ores.append(Ore("Flamakern", "Aesteria", "Withered Sand Layer", Tier.EXQUISITE, rarity_value=9050000))
        self.ores.append(Ore("Hallowed Cage", "Aesteria", "Withered Sand Layer", Tier.EXQUISITE, rarity_value=9050000))
        self.ores.append(Ore("Vitalium", "Aesteria", "Withered Sand Layer", Tier.EXQUISITE, rarity_value=14880000))
        self.ores.append(Ore("Arachnoxium", "Aesteria", "Withered Sand Layer", Tier.TRANSCENDENT, rarity_value=28800880))
        self.ores.append(Ore("Exsanguinatia", "Aesteria", "Withered Sand Layer", Tier.TRANSCENDENT, rarity_value=23893000))
        self.ores.append(Ore("Oculatum", "Aesteria", "Withered Sand Layer", Tier.TRANSCENDENT, rarity_value=32950000))
        self.ores.append(Ore("Ectoplasmado", "Aesteria", "Withered Sand Layer", Tier.ENIGMATIC, rarity_value=90770000))
        self.ores.append(Ore("Exospinel", "Aesteria", "Withered Sand Layer", Tier.ENIGMATIC, rarity_value=76763400))
        self.ores.append(Ore("CHTOTOZYOLE", "Aesteria", "Withered Sand Layer", Tier.UNFATHOMABLE, rarity_value=162901200))
        self.ores.append(Ore("Venemence", "Aesteria", "Withered Sand Layer", Tier.UNFATHOMABLE, rarity_value=475300660))
        
                                          
        self.ores.append(Ore("Candlelight", "Aesteria", "Hexafite Layer", Tier.EXOTIC, rarity_value=6670000))
        self.ores.append(Ore("Ghouleum", "Aesteria", "Hexafite Layer", Tier.EXOTIC, rarity_value=2801900))
        self.ores.append(Ore("Antipathy", "Aesteria", "Hexafite Layer", Tier.EXQUISITE, rarity_value=11700000))
        self.ores.append(Ore("Necrocrysta", "Aesteria", "Hexafite Layer", Tier.EXQUISITE, rarity_value=10235000))
        self.ores.append(Ore("Vexareign", "Aesteria", "Hexafite Layer", Tier.EXQUISITE, rarity_value=8839100))
        self.ores.append(Ore("Feux Follets", "Aesteria", "Hexafite Layer", Tier.TRANSCENDENT, rarity_value=40000000))
        self.ores.append(Ore("Nightmare Complex", "Aesteria", "Hexafite Layer", Tier.TRANSCENDENT, rarity_value=36667500))
        self.ores.append(Ore("Spiritbound Tomb", "Aesteria", "Hexafite Layer", Tier.TRANSCENDENT, rarity_value=30000000))
        self.ores.append(Ore("The All-Seeing", "Aesteria", "Hexafite Layer", Tier.TRANSCENDENT, rarity_value=32222222))
        self.ores.append(Ore("Poltergeist", "Aesteria", "Hexafite Layer", Tier.ENIGMATIC, rarity_value=89562220))
        self.ores.append(Ore("Soulshade", "Aesteria", "Hexafite Layer", Tier.ENIGMATIC, rarity_value=60928950))
        self.ores.append(Ore("Austiori", "Aesteria", "Hexafite Layer", Tier.UNFATHOMABLE, rarity_value=165390000))
        self.ores.append(Ore("Hallownest", "Aesteria", "Hexafite Layer", Tier.UNFATHOMABLE, rarity_value=312200300))
        
                                           
        self.ores.append(Ore("Glacius", "Aesteria", "Deepfrost Layer", Tier.EXOTIC, rarity_value=9750000))
        self.ores.append(Ore("Snowsled", "Aesteria", "Deepfrost Layer", Tier.EXOTIC, rarity_value=4400000))
        self.ores.append(Ore("Frostica", "Aesteria", "Deepfrost Layer", Tier.EXQUISITE, rarity_value=13000000))
        self.ores.append(Ore("Glacial Monolith", "Aesteria", "Deepfrost Layer", Tier.EXQUISITE, rarity_value=25000000))
        self.ores.append(Ore("Glaceiaflux", "Aesteria", "Deepfrost Layer", Tier.TRANSCENDENT, rarity_value=38800000))
        self.ores.append(Ore("Cryonstelar", "Aesteria", "Deepfrost Layer", Tier.TRANSCENDENT, rarity_value=53200000))
        self.ores.append(Ore("Divinis", "Aesteria", "Deepfrost Layer", Tier.ENIGMATIC, rarity_value=65318000))
        self.ores.append(Ore("Ephemryst", "Aesteria", "Deepfrost Layer", Tier.ENIGMATIC, rarity_value=275320000))
        
                                            
        self.ores.append(Ore("Pentaurunel", "Aesteria", "Jollystone Layer", Tier.EXOTIC, rarity_value=14500000))
        self.ores.append(Ore("Snowglobe II", "Aesteria", "Jollystone Layer", Tier.EXOTIC, rarity_value=4230000))
        self.ores.append(Ore("Luxe", "Aesteria", "Jollystone Layer", Tier.TRANSCENDENT, rarity_value=40000000))
        self.ores.append(Ore("The Express", "Aesteria", "Jollystone Layer", Tier.TRANSCENDENT, rarity_value=25260000))
        self.ores.append(Ore("Toyblast", "Aesteria", "Jollystone Layer", Tier.TRANSCENDENT, rarity_value=32190000))
        self.ores.append(Ore("Gelidoluar", "Aesteria", "Jollystone Layer", Tier.ENIGMATIC, rarity_value=78416000))
        self.ores.append(Ore("Yuletide Star", "Aesteria", "Jollystone Layer", Tier.ENIGMATIC, rarity_value=93580000))
        self.ores.append(Ore("Coruscentia", "Aesteria", "Jollystone Layer", Tier.UNFATHOMABLE, rarity_value=240800000))
        
                                          
        self.ores.append(Ore("Beachball", "Aesteria", "Maculite Layer", Tier.EXOTIC, rarity_value=2240000))
        self.ores.append(Ore("Sol", "Aesteria", "Maculite Layer", Tier.EXOTIC, rarity_value=7110000))
        self.ores.append(Ore("Dunestride", "Aesteria", "Maculite Layer", Tier.EXQUISITE, rarity_value=12938404))
        self.ores.append(Ore("Sunshade", "Aesteria", "Maculite Layer", Tier.EXQUISITE, rarity_value=8444000))
        self.ores.append(Ore("Sandstorm", "Aesteria", "Maculite Layer", Tier.TRANSCENDENT, rarity_value=27355200))
        self.ores.append(Ore("Sunlypse", "Aesteria", "Maculite Layer", Tier.TRANSCENDENT, rarity_value=39292929))
        self.ores.append(Ore("Lux Aestiva", "Aesteria", "Maculite Layer", Tier.ENIGMATIC, rarity_value=75524905))
        self.ores.append(Ore("Sunflower", "Aesteria", "Maculite Layer", Tier.ENIGMATIC, rarity_value=59204000))
        self.ores.append(Ore("Perihelion", "Aesteria", "Maculite Layer", Tier.UNFATHOMABLE, rarity_value=436000000))
        
                                          
        self.ores.append(Ore("Abyssium", "Aesteria", "Surmilum Layer", Tier.EXOTIC, rarity_value=5554555))
        self.ores.append(Ore("Floativite", "Aesteria", "Surmilum Layer", Tier.EXOTIC, rarity_value=3720880))
        self.ores.append(Ore("Sunsurf", "Aesteria", "Surmilum Layer", Tier.EXQUISITE, rarity_value=14250000))
        self.ores.append(Ore("Victide", "Aesteria", "Surmilum Layer", Tier.EXQUISITE, rarity_value=10000200))
        self.ores.append(Ore("Nautitan", "Aesteria", "Surmilum Layer", Tier.TRANSCENDENT, rarity_value=28424300))
        self.ores.append(Ore("Swirlpool", "Aesteria", "Surmilum Layer", Tier.TRANSCENDENT, rarity_value=44134560))
        self.ores.append(Ore("Frutiflux", "Aesteria", "Surmilum Layer", Tier.ENIGMATIC, rarity_value=90222015))
        self.ores.append(Ore("The Odyssey", "Aesteria", "Surmilum Layer", Tier.ENIGMATIC, rarity_value=61905731))
        self.ores.append(Ore("Subliminaire", "Aesteria", "Surmilum Layer", Tier.UNFATHOMABLE, rarity_value=505505505))
        
                                            
        self.ores.append(Ore("Bloodshot", "Aesteria", "Sugarstone Layer", Tier.EXOTIC, rarity_value=6302204))
        self.ores.append(Ore("Witchbroom", "Aesteria", "Sugarstone Layer", Tier.EXOTIC, rarity_value=3335000))
        self.ores.append(Ore("Spectrasoul", "Aesteria", "Sugarstone Layer", Tier.EXQUISITE, rarity_value=9103204))
        self.ores.append(Ore("Venurbite", "Aesteria", "Sugarstone Layer", Tier.EXQUISITE, rarity_value=12250000))
        self.ores.append(Ore("Hollowed", "Aesteria", "Sugarstone Layer", Tier.TRANSCENDENT, rarity_value=45554555))
        self.ores.append(Ore("Praefectus", "Aesteria", "Sugarstone Layer", Tier.TRANSCENDENT, rarity_value=29292900))
        self.ores.append(Ore("Spectrus", "Aesteria", "Sugarstone Layer", Tier.TRANSCENDENT, rarity_value=22185000))
        self.ores.append(Ore("Celestival", "Aesteria", "Sugarstone Layer", Tier.ENIGMATIC, rarity_value=76767767))
        self.ores.append(Ore("The Flying Dutchman", "Aesteria", "Sugarstone Layer", Tier.ENIGMATIC, rarity_value=92210000))
        self.ores.append(Ore("Velrathis", "Aesteria", "Sugarstone Layer", Tier.ENIGMATIC, rarity_value=50100000))
        self.ores.append(Ore("UNFUN", "Aesteria", "Sugarstone Layer", Tier.UNFATHOMABLE, rarity_value=188235155))
        self.ores.append(Ore("Vocarus", "Aesteria", "Sugarstone Layer", Tier.UNFATHOMABLE, rarity_value=335191400))
        
                                            
        self.ores.append(Ore("Eyemalgam", "Aesteria", "Delucemite Layer", Tier.EXOTIC, rarity_value=6246575))
        self.ores.append(Ore("Tombstone", "Aesteria", "Delucemite Layer", Tier.EXOTIC, rarity_value=2111111))
        self.ores.append(Ore("Silverthorn", "Aesteria", "Delucemite Layer", Tier.EXQUISITE, rarity_value=14343235))
        self.ores.append(Ore("Soulsnare", "Aesteria", "Delucemite Layer", Tier.EXQUISITE, rarity_value=11230050))
        self.ores.append(Ore("Aphantasia", "Aesteria", "Delucemite Layer", Tier.TRANSCENDENT, rarity_value=41200000))
        self.ores.append(Ore("Apparition", "Aesteria", "Delucemite Layer", Tier.TRANSCENDENT, rarity_value=48900000))
        self.ores.append(Ore("Corerupted", "Aesteria", "Delucemite Layer", Tier.TRANSCENDENT, rarity_value=35300250))
        self.ores.append(Ore("Trudgium", "Aesteria", "Delucemite Layer", Tier.TRANSCENDENT, rarity_value=28750450))
        self.ores.append(Ore("Lucifyx", "Aesteria", "Delucemite Layer", Tier.ENIGMATIC, rarity_value=66666666))
        self.ores.append(Ore("Umbrasnare", "Aesteria", "Delucemite Layer", Tier.ENIGMATIC, rarity_value=89945000))
        self.ores.append(Ore("Grimonolith", "Aesteria", "Delucemite Layer", Tier.UNFATHOMABLE, rarity_value=385765000))
        self.ores.append(Ore("Sombermoor", "Aesteria", "Delucemite Layer", Tier.UNFATHOMABLE, rarity_value=516734005))
        self.ores.append(Ore("Overseer", "Aesteria", "Delucemite Layer", Tier.OTHERWORLDLY, rarity_value=977737207))
        
                                       
        self.ores.append(Ore("Boreas", "Aesteria", "Frost Layer", Tier.EXOTIC, rarity_value=4300000))
        self.ores.append(Ore("Nixalis", "Aesteria", "Frost Layer", Tier.EXOTIC, rarity_value=2000000))
        self.ores.append(Ore("Festivian", "Aesteria", "Frost Layer", Tier.EXQUISITE, rarity_value=13500000))
        self.ores.append(Ore("Noctilucite", "Aesteria", "Frost Layer", Tier.EXQUISITE, rarity_value=7700000))
        self.ores.append(Ore("Behemoth Snowflake", "Aesteria", "Frost Layer", Tier.TRANSCENDENT, rarity_value=30000000))
        self.ores.append(Ore("Dynafrost", "Aesteria", "Frost Layer", Tier.TRANSCENDENT, rarity_value=42000000))
        self.ores.append(Ore("North Star", "Aesteria", "Frost Layer", Tier.TRANSCENDENT, rarity_value=21980000))
        self.ores.append(Ore("Aurora Polaris", "Aesteria", "Frost Layer", Tier.ENIGMATIC, rarity_value=15000000))
        self.ores.append(Ore("Noxilenciosa", "Aesteria", "Frost Layer", Tier.ENIGMATIC, rarity_value=55000000))
        self.ores.append(Ore("The North Pole", "Aesteria", "Frost Layer", Tier.ENIGMATIC, rarity_value=90135000))
        self.ores.append(Ore("Frostblossom", "Aesteria", "Frost Layer", Tier.UNFATHOMABLE, rarity_value=183640000))
        
                                      
                       
        self.ores.append(Ore("Blood Lunarian", "Aesteria", "Cave Exclusive", Tier.EXQUISITE, rarity_value=1606636, is_cave_exclusive=True, cave_type="Soulseek"))
        self.ores.append(Ore("Amalton", "Aesteria", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=2529420, is_cave_exclusive=True, cave_type="Soulseek"))
        self.ores.append(Ore("Heretic's Cage", "Aesteria", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=7425240, is_cave_exclusive=True, cave_type="Soulseek"))
                          
        self.ores.append(Ore("Lovestruck", "Aesteria", "Cave Exclusive", Tier.EXOTIC, rarity_value=1010101, is_cave_exclusive=True, cave_type="Heartstring"))
        self.ores.append(Ore("Amorisene", "Aesteria", "Cave Exclusive", Tier.ENIGMATIC, rarity_value=9285714, is_cave_exclusive=True, cave_type="Heartstring"))
                        
        self.ores.append(Ore("Cursed Flesh", "Aesteria", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=843000, is_cave_exclusive=True, cave_type="Fractured"))
        self.ores.append(Ore("Bathophobia", "Aesteria", "Cave Exclusive", Tier.TRANSCENDENT, rarity_value=1000000, is_cave_exclusive=True, cave_type="Fractured"))
        
                         
                                           
        self.ores.append(Ore("Charliment", "Lucernia", "Lucitreum Layer", Tier.EXOTIC, rarity_value=2700100))
        self.ores.append(Ore("Luna", "Lucernia", "Lucitreum Layer", Tier.EXOTIC, rarity_value=5000005))
        self.ores.append(Ore("Gelisol", "Lucernia", "Lucitreum Layer", Tier.EXQUISITE, rarity_value=9100999))
        self.ores.append(Ore("Lyricarol", "Lucernia", "Lucitreum Layer", Tier.EXQUISITE, rarity_value=12030000))
        self.ores.append(Ore("Snowglobe III", "Lucernia", "Lucitreum Layer", Tier.TRANSCENDENT, rarity_value=44320000))
        self.ores.append(Ore("Xuě", "Lucernia", "Lucitreum Layer", Tier.TRANSCENDENT, rarity_value=19199991))
        self.ores.append(Ore("Borealiheim", "Lucernia", "Lucitreum Layer", Tier.ENIGMATIC, rarity_value=91000000))
        self.ores.append(Ore("Crystalia", "Lucernia", "Lucitreum Layer", Tier.ENIGMATIC, rarity_value=61100160))
        self.ores.append(Ore("Tsukilunica", "Lucernia", "Lucitreum Layer", Tier.ENIGMATIC, rarity_value=74503550))
        self.ores.append(Ore("Wishtree", "Lucernia", "Lucitreum Layer", Tier.UNFATHOMABLE, rarity_value=403320250))
        self.ores.append(Ore("Yuki Onna", "Lucernia", "Lucitreum Layer", Tier.UNFATHOMABLE, rarity_value=532100335))
        
                                           
        self.ores.append(Ore("Glaciamoria", "Lucernia", "Cicallite Layer", Tier.EXOTIC, rarity_value=5000000))
        self.ores.append(Ore("Mr. Frosty", "Lucernia", "Cicallite Layer", Tier.EXOTIC, rarity_value=4000000))
        self.ores.append(Ore("Winterlark", "Lucernia", "Cicallite Layer", Tier.EXOTIC, rarity_value=3000000))
        self.ores.append(Ore("Aesrith", "Lucernia", "Cicallite Layer", Tier.EXQUISITE, rarity_value=11029000))
        self.ores.append(Ore("Frostbite", "Lucernia", "Cicallite Layer", Tier.EXQUISITE, rarity_value=14442444))
        self.ores.append(Ore("Antlerice", "Lucernia", "Cicallite Layer", Tier.TRANSCENDENT, rarity_value=30100200))
        self.ores.append(Ore("Froidure", "Lucernia", "Cicallite Layer", Tier.TRANSCENDENT, rarity_value=28200911))
        self.ores.append(Ore("Cryoscope", "Lucernia", "Cicallite Layer", Tier.ENIGMATIC, rarity_value=84100299))
        self.ores.append(Ore("Frostress", "Lucernia", "Cicallite Layer", Tier.ENIGMATIC, rarity_value=55192555))
        self.ores.append(Ore("Polaris", "Lucernia", "Cicallite Layer", Tier.ENIGMATIC, rarity_value=62626626))
        self.ores.append(Ore("Cocytus", "Lucernia", "Cicallite Layer", Tier.UNFATHOMABLE, rarity_value=233114000))
        self.ores.append(Ore("Polarctica", "Lucernia", "Cicallite Layer", Tier.UNFATHOMABLE, rarity_value=686019200))
        
                                            
        self.ores.append(Ore("Jinglelyn", "Lucernia", "Confectent Layer", Tier.EXOTIC, rarity_value=3200000))
        self.ores.append(Ore("Kindleflame", "Lucernia", "Confectent Layer", Tier.EXOTIC, rarity_value=6000200))
        self.ores.append(Ore("Twinkle Star", "Lucernia", "Confectent Layer", Tier.EXOTIC, rarity_value=2500000))
        self.ores.append(Ore("Festivatia", "Lucernia", "Confectent Layer", Tier.EXQUISITE, rarity_value=8100200))
        self.ores.append(Ore("Luminaria", "Lucernia", "Confectent Layer", Tier.EXQUISITE, rarity_value=10020020))
        self.ores.append(Ore("Chandelabra", "Lucernia", "Confectent Layer", Tier.TRANSCENDENT, rarity_value=24029990))
        self.ores.append(Ore("Ornaswirl", "Lucernia", "Confectent Layer", Tier.TRANSCENDENT, rarity_value=41888888))
        self.ores.append(Ore("Algifica", "Lucernia", "Confectent Layer", Tier.ENIGMATIC, rarity_value=52000000))
        self.ores.append(Ore("Angelicus", "Lucernia", "Confectent Layer", Tier.ENIGMATIC, rarity_value=66100204))
        self.ores.append(Ore("Verdafrost", "Lucernia", "Confectent Layer", Tier.ENIGMATIC, rarity_value=77777777))
        self.ores.append(Ore("Asminthia", "Lucernia", "Confectent Layer", Tier.UNFATHOMABLE, rarity_value=355200400))
        self.ores.append(Ore("Wintburg", "Lucernia", "Confectent Layer", Tier.UNFATHOMABLE, rarity_value=732349090))
        
                                           
        self.ores.append(Ore("Acore", "Lucernia", "Foligrass Layer", Tier.EXOTIC, rarity_value=6500200))
        self.ores.append(Ore("Leaffall", "Lucernia", "Foligrass Layer", Tier.EXOTIC, rarity_value=3300000))
        self.ores.append(Ore("Clementium", "Lucernia", "Foligrass Layer", Tier.EXQUISITE, rarity_value=9700120))
        self.ores.append(Ore("Harvestine", "Lucernia", "Foligrass Layer", Tier.EXQUISITE, rarity_value=13400200))
        self.ores.append(Ore("Harvest Moon", "Lucernia", "Foligrass Layer", Tier.TRANSCENDENT, rarity_value=19500300))
        self.ores.append(Ore("Herbst", "Lucernia", "Foligrass Layer", Tier.TRANSCENDENT, rarity_value=29600100))
        self.ores.append(Ore("Wanwood", "Lucernia", "Foligrass Layer", Tier.TRANSCENDENT, rarity_value=40000000))
        self.ores.append(Ore("Cobbore", "Lucernia", "Foligrass Layer", Tier.ENIGMATIC, rarity_value=83200200))
        self.ores.append(Ore("Maplefall", "Lucernia", "Foligrass Layer", Tier.ENIGMATIC, rarity_value=62001290))
        self.ores.append(Ore("Autumnus", "Lucernia", "Foligrass Layer", Tier.UNFATHOMABLE, rarity_value=240100000))
        self.ores.append(Ore("Reminiscence", "Lucernia", "Foligrass Layer", Tier.UNFATHOMABLE, rarity_value=390100600))
        
                                           
        self.ores.append(Ore("Rot Monolith", "Lucernia", "Sepulcrum Layer", Tier.EXOTIC, rarity_value=7264513))
        self.ores.append(Ore("Wraith", "Lucernia", "Sepulcrum Layer", Tier.EXOTIC, rarity_value=3724561))
        self.ores.append(Ore("Itomidori", "Lucernia", "Sepulcrum Layer", Tier.EXQUISITE, rarity_value=7500001))
        self.ores.append(Ore("Whirliwisp", "Lucernia", "Sepulcrum Layer", Tier.EXQUISITE, rarity_value=14999999))
        self.ores.append(Ore("Morichronica", "Lucernia", "Sepulcrum Layer", Tier.TRANSCENDENT, rarity_value=47250000))
        self.ores.append(Ore("Pale Love", "Lucernia", "Sepulcrum Layer", Tier.TRANSCENDENT, rarity_value=22304999))
        self.ores.append(Ore("Soulswirl", "Lucernia", "Sepulcrum Layer", Tier.TRANSCENDENT, rarity_value=36443000))
        self.ores.append(Ore("It.", "Lucernia", "Sepulcrum Layer", Tier.ENIGMATIC, rarity_value=76000000))
        self.ores.append(Ore("Keres", "Lucernia", "Sepulcrum Layer", Tier.ENIGMATIC, rarity_value=94000000))
        self.ores.append(Ore("The Sludge", "Lucernia", "Sepulcrum Layer", Tier.ENIGMATIC, rarity_value=52000000))
        self.ores.append(Ore("Derelictum", "Lucernia", "Sepulcrum Layer", Tier.UNFATHOMABLE, rarity_value=710000000))
        self.ores.append(Ore("Midnight", "Lucernia", "Sepulcrum Layer", Tier.UNFATHOMABLE, rarity_value=490001200))
        
                                          
        self.ores.append(Ore("Sigilite", "Lucernia", "Wickrock Layer", Tier.EXOTIC, rarity_value=6666666))
        self.ores.append(Ore("SMILE", "Lucernia", "Wickrock Layer", Tier.EXOTIC, rarity_value=3666666))
        self.ores.append(Ore("Diavitura", "Lucernia", "Wickrock Layer", Tier.EXQUISITE, rarity_value=12666666))
        self.ores.append(Ore("Ritualismium", "Lucernia", "Wickrock Layer", Tier.EXQUISITE, rarity_value=8666666))
        self.ores.append(Ore("Moon Fragment", "Lucernia", "Wickrock Layer", Tier.TRANSCENDENT, rarity_value=36666666))
        self.ores.append(Ore("Vlasovale", "Lucernia", "Wickrock Layer", Tier.TRANSCENDENT, rarity_value=26666666))
        self.ores.append(Ore("Praecantatus", "Lucernia", "Wickrock Layer", Tier.ENIGMATIC, rarity_value=66666666))
        self.ores.append(Ore("Sacrilege", "Lucernia", "Wickrock Layer", Tier.ENIGMATIC, rarity_value=86666666))
        self.ores.append(Ore("Sinstar", "Lucernia", "Wickrock Layer", Tier.ENIGMATIC, rarity_value=56666666))
        self.ores.append(Ore("Underworld", "Lucernia", "Wickrock Layer", Tier.UNFATHOMABLE, rarity_value=666666666))
        self.ores.append(Ore("IBLIS", "Lucernia", "Wickrock Layer", Tier.OTHERWORLDLY, rarity_value=1666666666))
        
                                      
                       
        self.ores.append(Ore("Celebration", "Lucernia", "Cave Exclusive", Tier.EXOTIC, rarity_value=265957, is_cave_exclusive=True, cave_type="Firework"))
    
    def get_all_ores(self) -> List[Ore]:
                          
        return self.ores.copy()
    
    def get_ores_by_world(self, world: str) -> List[Ore]:
                                                
        return [ore for ore in self.ores if ore.world == world]
    
    def get_ores_by_layer(self, world: str, layer: str) -> List[Ore]:
                                                          
        return [ore for ore in self.ores 
                if ore.world == world and ore.layer == layer]
    
    def get_ore_by_name(self, name: str) -> Optional[Ore]:
                                    
        for ore in self.ores:
            if ore.name == name:
                return ore
        return None
    
    def get_worlds(self) -> List[str]:
                                           
        preferred_order = [
            "Natura",
            "Caverna",
            "Digita",
            "Luna Refuge",
            "Aesteria",
            "Lucernia",
        ]
        worlds = list(sorted(set(ore.world for ore in self.ores)))
        ordered = [w for w in preferred_order if w in worlds]
        remaining = [w for w in worlds if w not in set(ordered)]
        return ordered + remaining
    
    def get_layers(self, world: str) -> List[str]:
                                                                                    
                                           
        layer_orders = {
            "Natura": [
                "World Exclusive",
                "Stone Layer",
                "Basalt Layer",
                "Granite Layer",
                "Diorite Layer",
                "Obsidian Layer",
                "Marble Layer",
                "Mantle Layer",
                "Outer Core Layer",
                "Inner Core Layer"
            ],
            "Caverna": [
                "Slate Layer",
                "Permafrost Layer",
                "Shatterstone Layer",
                "Riftrock Layer",
                "Darkmatter Layer",
                "Void Layer"
            ],
            "Digita": [
                "Statistone Layer",
                "Wireframe Layer",
                "Matricite Layer",
                "Mechaloid Layer",
                "Steel Layer",
                "Penumbrum Layer",
                "Twilement Layer",
                "Cosmorock Layer",
                "Glitch Layer",
                "Virus Layer"
            ],
            "Luna Refuge": [
                "Moon Stone Layer",
                "Moon Mantle Layer",
                "Moon Core Layer",
                "Rocc Layer"
            ],
            "Aesteria": [
                "Spookstone Layer",
                "Affement Layer",
                "Withered Sand Layer",
                "Hexafite Layer",
                "Deepfrost Layer",
                "Jollystone Layer",
                "Maculite Layer",
                "Surmilum Layer",
                "Sugarstone Layer",
                "Delucemite Layer",
                "Frost Layer"
            ],
            "Lucernia": [
                "Lucitreum Layer",
                "Cicallite Layer",
                "Confectent Layer",
                "Foligrass Layer",
                "Sepulcrum Layer",
                "Wickrock Layer"
            ]
        }
        
                                             
        available_layers = set(ore.layer for ore in self.ores if ore.world == world)
        
                                                           
        if world in layer_orders:
            ordered = [layer for layer in layer_orders[world] if layer in available_layers]
                                                                                               
            remaining = sorted(available_layers - set(ordered))
            return ordered + remaining
        
                                                     
        return sorted(available_layers)
    
    def get_cave_types(self, world: Optional[str] = None) -> List[str]:
                                                                         
        cave_types = set()
        for ore in self.ores:
            if ore.is_cave_exclusive and ore.cave_type:
                if world is None or ore.world == world:
                    cave_types.add(ore.cave_type)
        return sorted(list(cave_types))
    
    def filter_ores(self, world: Optional[str] = None, 
                   layer: Optional[str] = None,
                   is_cave_exclusive: Optional[bool] = None,
                   cave_type: Optional[str] = None,
                   search_term: Optional[str] = None) -> List[Ore]:
                                             
        filtered = self.ores.copy()
        
        if world:
            filtered = [ore for ore in filtered if ore.world == world]
        
        if layer:
            filtered = [ore for ore in filtered if ore.layer == layer]
        
        if is_cave_exclusive is not None:
            filtered = [ore for ore in filtered 
                       if ore.is_cave_exclusive == is_cave_exclusive]
        
        if cave_type:
            filtered = [ore for ore in filtered 
                       if ore.cave_type == cave_type]
        
        if search_term:
            search_lower = search_term.lower()
            filtered = [ore for ore in filtered 
                       if search_lower in ore.name.lower()]
        
        return filtered
    
    @staticmethod
    def get_tier_order() -> Dict[Tier, int]:
                                                           
        return {
            Tier.LAYER: 0,
            Tier.COMMON: 1,
            Tier.UNCOMMON: 2,
            Tier.RARE: 3,
            Tier.MASTER: 4,
            Tier.SURREAL: 5,
            Tier.MYTHIC: 6,
            Tier.EXOTIC: 7,
            Tier.EXQUISITE: 8,
            Tier.TRANSCENDENT: 9,
            Tier.ENIGMATIC: 10,
            Tier.UNFATHOMABLE: 11,
            Tier.OTHERWORLDLY: 12,
            Tier.ZENITH: 13,
            Tier.EXCLUSIVE: 14,
        }
    
    def get_statistics(self, tracked_ores: Dict[str, bool]) -> Dict:
                                               
        total = len(self.ores)
        found = sum(1 for ore in self.ores if tracked_ores.get(ore.name, False))
        
                              
        world_stats = {}
        for ore in self.ores:
            if ore.world not in world_stats:
                world_stats[ore.world] = {"total": 0, "found": 0}
            world_stats[ore.world]["total"] += 1
            if tracked_ores.get(ore.name, False):
                world_stats[ore.world]["found"] += 1
        
                             
        tier_stats = {}
        for ore in self.ores:
            tier_name = ore.tier.value
            if tier_name not in tier_stats:
                tier_stats[tier_name] = {"total": 0, "found": 0}
            tier_stats[tier_name]["total"] += 1
            if tracked_ores.get(ore.name, False):
                tier_stats[tier_name]["found"] += 1
        
        return {
            "total": total,
            "found": found,
            "percentage": (found / total * 100) if total > 0 else 0,
            "world_stats": world_stats,
            "tier_stats": tier_stats,
        }


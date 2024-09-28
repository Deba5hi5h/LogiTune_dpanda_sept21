from dataclasses import dataclass


@dataclass
class StreamingLightInfo:
    name: str
    project_name: str


streaming_light_info_set = [
    StreamingLightInfo('Litra Beam', 'litra_beam'),
    StreamingLightInfo('Litra Glow', 'litra_glow'),
]

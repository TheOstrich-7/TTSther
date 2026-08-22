import pykokoro
"""
degrees of freedom/features
    voices
        voice blending
    model
    model quality
    language
    speed
    pause config
    scapy
    trim
    short sentences
    seed
"""

test = pykokoro.KokoroPipeline(pykokoro.PipelineConfig(voice="af_sarah", model_source="huggingface", model_variant="v1.0", model_quality="q8"))

print(test.synth._kokoro.get_voices())
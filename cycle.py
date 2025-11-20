def get_cycle_phase(cycle_length, day):
    follicular = cycle_length * 0.45
    ovulation = cycle_length * 0.1

    if day <= follicular:
        return "生理〜卵胞期（メンタル安定しやすい）"
    elif day <= follicular + ovulation:
        return "排卵期（食欲低め・代謝普通）"
    else:
        return "黄体期（むくみ・食欲↑・代謝微増）"

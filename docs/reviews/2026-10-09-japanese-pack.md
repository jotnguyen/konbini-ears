# Review: `ja-service.yaml`, 2026-10-09

An adversarial review by a separate agent, briefed to act as a fluent speaker who has worked
Japanese service jobs. It was read-only and was told to find what's wrong, not to praise.

**Verdict:** the Japanese is natural, the keigo level is right, and every kana reading checked out:
numbers, the 膳 and 名様 counters, rendaku, and しちじ for 7時. The real problems were in how
answers are judged, plus a few trap or outdated lines.

## Changes made

| Finding | Fix |
|---|---|
| Plain いらっしゃいませ and ありがとうございました appear in several scenes with different English meanings, so a learner could be offered two correct-sounding choices and marked wrong. | **Code:** a step that shares any Japanese line with the current one never supplies a wrong answer (`choicesFor` in `web/template.html`; see D8 in `DECISIONS.md`). **Pack:** greetings unified to "Welcome!" and goodbyes to "Thank you!"; the またお越しください variants say "Thank you, please come again". |
| `kb-receipt`: レシートはよろしいですか means "you're fine *without* it?", so はい means no receipt. | That variant now has its own meaning, plus a trap note. The reply is now レシートください, which always works. |
| `rm-rich`: flavor strength is 薄め/濃いめ (lighter/stronger), not 少なめ/多め (less/more). | Replies: 普通で, 薄めで, 濃いめで, 油少なめで. |
| `rs-smoke`: smoking or non-smoking seats is a pre-2020 question. | Replaced with 店内は全席禁煙となっております ("the whole place is non-smoking"); `p` lowered to 0.1. |
| 吸いません ("I don't smoke") sounds just like すいません ("excuse me"). | The reply is now 吸わないです. |
| `sh-bag`: 大丈夫です after "is that OK?" can mean "fine, I'll pay". | The reply is now 袋はいらないです, with a note explaining why. |
| Near-synonym meanings across scenes (passport ×2, bag ×2, drink ×4, "ready to order" ×2). | Meanings made distinct, e.g. "(for tax-free)" vs "(hotel check-in)". お決まりでしたらどうぞ became the more usual …お伺いします. |
| `kb-age` never mentioned age. | 年齢確認のため、画面のタッチをお願いします. |
| Tax-free switches to a refund model on 1 Nov 2026. | Note added on `sh-taxfree`. |
| Smaller fixes: the 差して key, the …円からお預かりします variant, the アプリ point-card variant, 替え玉 is asked for rather than offered, iekei お好み, a softer もう少し待ってもらえますか, どのくらい待ちますか, and ご試着なさいますか (instead of the mixed-keigo ご試着されますか). | All applied. |

## Lines added (the reviewer's "missing high-frequency" list)

- Choosing payment on the screen, and paying at a machine (`kb-pay`)
- 一括 one-time payment (`sh-taxfree`)
- ご予約はされていますか (`rs-count`)
- お通し, as a new step (`rs-otoshi`)
- Water is self-service (`rs-seat`)
- お待たせしました、熱いので… as a new step (`rm-serve`)
- Check-in from 15:00 (`ht-breakfast`)

## Not verified

The reviewer is a model, not a native speaker. The fixes are standard service Japanese and pass
the OpenJTalk reading check, but nobody has heard them in a real shop yet. KE-001 (the trip notes)
is the real-world check.

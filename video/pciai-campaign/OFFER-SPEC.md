# FOUNDINGFREE — what must be true before these films go out

The campaign promises a working promo code. If the code is missing or
misconfigured, every view lands on a failure, and a failed code on a
credential body reads as a scam rather than a bug. So this was checked against
the platform source rather than assumed.

**Nothing below is a recommendation about the offer itself — that is PCI's
decision. It is the configuration the offer needs in order to behave the way
the films say it does.**

## The good news: the platform already does exactly this

`backend/schema.sql` describes founding-stage access as a *"100% fee waiver
layered over the paid flow … a valid code grants membership + study + exam
together"*. That is precisely the offer — free membership and free exam
enrolment — and it is a first-class feature, not something bolted on.

Route 1 (`POST /api/founding/redeem`, `backend/Endpoints/Founding.cs:203`)
grants it with no application and no evidence, immediately.

## The configuration the code needs

Create it in the admin console as a discount code with:

| Column | Value | Why this exact value |
|---|---|---|
| `code` | **`FOUNDINGFREE`** — capitals | See the warning below. This one will bite. |
| `founding_route` | `founding` | A code with this empty is invisible to the founding lookup (`Founding.cs:167`) and returns `invalid_code` however correct it looks in the admin list. |
| `grants_membership` | `1` | "free membership" |
| `grants_exam` | `1` | "free exam enrolment" |
| `grants_study_access` | `1` | Included in the same waiver; withholding it would make the exam grant hollow. |
| `requires_application` | `0` | At `1` the user is sent to an evidence-upload flow that may sit in `pending_review`. The films promise immediate access, so this must be `0` or the promise breaks. |
| `active` | `1` | `Usable()` rejects anything else outright. |
| `start_date` | blank, or on/before launch day | A future date returns `not_open`. |
| `end_date` | the campaign end, or blank | A date-only value is treated as inclusive to `23:59:59`, so the last day works in full. |
| `max_uses` | a deliberate number, or blank for unlimited | On reaching the cap the API returns `fully_redeemed` — distinct from `invalid_code`, so users are told the truth. Decide this deliberately: a cap hit mid-campaign turns paid reach into a dead end. |
| `per_user_limit` / `single_use_per_email` | your call | Not required for the films to be accurate. |

## ⚠️ The code must be stored in CAPITALS

`Founding.cs:167` uppercases whatever the user types before it queries:

```csharp
db.QueryOne("SELECT * FROM discount_codes WHERE code=? AND founding_route IS NOT NULL AND founding_route!=''",
            code.Trim().ToUpperInvariant())
```

The lookup is therefore always for `FOUNDINGFREE`. A code stored as
`Foundingfree` — exactly as it was written in the brief — **will never match**,
and every person who types it correctly will be told their code is invalid.

The films show the code as `FOUNDINGFREE` in capitals for this reason. It is
also how promo codes are conventionally set, so nothing is lost.

The upside of that same line: because input is uppercased and trimmed, a user
typing `foundingfree`, `Foundingfree` or ` FoundingFree ` all succeed. Only the
**stored** value has to be capitals.

## One thing the films must not imply

Redemption requires a signed-in account — `/api/founding/redeem` returns
`401 no_token` otherwise. The journey is **create an account, then apply the
code**, not "enter a code and you are in".

The films therefore say *"apply code FOUNDINGFREE"* against a named page rather
than implying one-step instant enrolment, and the landing page
`route-founding.html` already exists to receive them.

## Before launch — a 60-second check

1. Create the code as specified above.
2. Register a throwaway account on the live site.
3. `POST /api/founding/redeem` with `{"code":"foundingfree"}` — deliberately
   lower case, to prove the uppercasing path works end to end.
4. Expect `{ ok: true, granted: { membership: true, exam: true, study: true } }`.
5. Confirm the account actually shows membership and exam access.

If step 4 returns `invalid_code`, the cause is almost certainly `founding_route`
being empty or the stored code not being capitals.

#!/usr/bin/env python3
"""
Narration, one entry per beat, placed at that beat's own start time.

Why per beat rather than one continuous read: the ten films are already
rendered and their beat timings are fixed, so the voice has to meet the
picture rather than the other way round. Generating per beat and placing each
segment at its beat start keeps the voice locked to the cut — and on the 4:5
films, locked to the burned caption, which is the mismatch a viewer actually
notices.

Lengths are written to fit. Natural narration runs ~2.3 words/second, so each
beat's budget is its duration x 2.3, and these sit at roughly 80% of that:
a line that overruns its slot is what makes narration sound hurried, and on a
30-second reel there is nowhere for the overflow to go.

On the reels the voice does NOT read the type back — the type is already the
message, and hearing the same words you are reading is the flattest thing a
film can do. It carries the argument underneath instead.
"""

# film: (duration, [(beat_id, beat_start, text), ...])
SCRIPTS = {
 'r1': (26.00, [
   ('b1', 0.00, "AI just wrote your schedule. Cost-loaded. Levelled."),
   ('b2', 3.30, "It will not sign it. A person does — the one whose name is on the forecast."),
   ('b3', 7.60, "AI proposes. The professional disposes. That is the whole principle."),
   ('b4', 12.90, "Three credentials for that professional. Thirteen domains. Every one publicly verifiable."),
   ('b5', 19.30, "Founding enrolment is open. Apply code FOUNDINGFREE — membership, study and exam, free."),
 ]),
 'r2': (30.40, [
   ('b1', 0.00, "Three credentials. Most people only need one."),
   ('b2', 4.40, "PCL-AI, the flagship. This is yours if you own the schedule and the cost picture together."),
   ('b3', 11.00, "PFL-AI, the money side. Yours if the forecast and the cost report carry your name."),
   ('b4', 17.60, "PML-AI, delivery. Yours if you run the programme itself — scope, risk and change."),
   ('b5', 24.20, "Whichever one is yours, founding enrolment is open. Create an account, then apply FOUNDINGFREE."),
 ]),
 'r3': (30.00, [
   ('b1', 0.00, "Before you pay for any credential, ask what the exam actually assesses."),
   ('b2', 4.30, "Thirteen domains, published in full. The exam is sampled from them."),
   ('b3', 11.20, "Budgeting. Earned value. Scheduling. Risk. And AI for project controls itself."),
   ('b4', 16.40, "What all thirteen are testing is judgement over AI output. Not recall."),
   ('b5', 21.60, "Founding enrolment is open. Apply code FOUNDINGFREE — membership, study and exam, free."),
 ]),
 'r4': (30.00, [
   ('b1', 0.00, "That credential on their CV. Could you check it? Right now, in a browser."),
   ('b2', 4.40, "If not, you are not checking anything. You are trusting the typing."),
   ('b3', 9.60, "A credential that cannot be checked is not a credential."),
   ('b4', 14.20, "So ours can be. Look up the reference, and the record answers. This example is invented."),
   ('b5', 21.80, "Get one that checks out. Apply code FOUNDINGFREE — membership, study and exam enrolment, free."),
 ]),
 'r5': (34.00, [
   ('b1', 0.00, "The forecast is written. You still sign it. The skill that matters has moved."),
   ('b2', 4.70, "Three credentials for that judgement. Controls, finance, and delivery."),
   ('b3', 9.70, "One body of knowledge behind them. Assessed, then publicly verifiable."),
   ('b4', 14.30, "Why is founding enrolment free? Because it is early. For that reason and no other."),
   ('b5', 19.10, "No countdown. No last places. Nothing here runs out while you decide."),
   ('b6', 23.10, "Apply code FOUNDINGFREE — free membership, study access and exam enrolment, on a PCI account."),
   ('b7', 29.20, "Create an account, sign in, apply the code. Info at pciai dot org."),
 ]),
 'v1': (44.00, [
   ('b1', 0.00, "AI just wrote your schedule. Cost-loaded, resource-levelled, in about four seconds."),
   ('b2', 4.20, "It will not sign it. A person does — the one whose name is on the forecast when the board asks why."),
   ('b3', 9.00, "A model cannot know the assumption nobody wrote down, or tell you the float is not really there."),
   ('b4', 17.40, "AI proposes. The professional disposes. That is our governing principle."),
   ('b5', 23.60, "So we built the standard for that judgement. Three credentials, thirteen domains, publicly verifiable."),
   ('b6', 33.40, "Founding enrolment is open. Apply code FOUNDINGFREE — membership, study and exam, free. Info at pciai dot org."),
 ]),
 'v2': (48.60, [
   ('b1', 0.00, "Three credentials. Which one is yours?"),
   ('b2', 4.60, "PCL-AI, the flagship. This is you if you own the cost baseline and the schedule under it."),
   ('b3', 13.20, "PFL-AI. This is you if the forecast goes out with your name on it."),
   ('b4', 21.80, "PML-AI. This is you if the programme is yours — scope, risk and change."),
   ('b5', 30.40, "The baseline, PCL-AI. The forecast, PFL-AI. The programme, PML-AI. All three, thirteen domains, publicly verifiable."),
   ('b6', 39.00, "Whichever is yours, founding enrolment is open. Apply code FOUNDINGFREE. Info at pciai dot org."),
 ]),
 'v3': (46.00, [
   ('b1', 0.00, "One question is worth asking before you pay for any credential. What does the exam actually assess?"),
   ('b2', 5.40, "For PCL-AI the body of knowledge is published in full. Thirteen domains, and the exam is sampled from them."),
   ('b3', 12.60, "You can read them. Budgeting and forecasting. Scheduling. Risk. And AI for project controls itself."),
   ('b4', 19.00, "Every one tests the same thing, and it is not memory. A model hands you a forecast. The work is knowing when it is wrong, and defending the call."),
   ('b5', 28.60, "AI proposes. The professional disposes. That principle is why the syllabus looks like this."),
   ('b6', 35.20, "Founding enrolment is open. Apply code FOUNDINGFREE — membership, study and exam, free. Info at pciai dot org."),
 ]),
 'v4': (50.60, [
   ('b1', 0.00, "Anyone can type a credential. Typing one takes a second. Earning one does not."),
   ('b2', 6.60, "A CV shows you a name. A body. A date. None of that is evidence. It is formatting."),
   ('b3', 15.60, "So when you read it, you are not checking a credential. You are trusting the typing."),
   ('b4', 21.40, "A credential that cannot be checked is just a claim. That is the rule we hold ourselves to."),
   ('b5', 27.60, "So ours can be checked, publicly, by anyone. Look up the reference, and the record answers."),
   ('b6', 36.00, "And it cuts both ways. Nobody takes your word for it, and you are not left hoping they believe you."),
   ('b7', 44.60, "Founding enrolment is open. Get one that checks out. Apply code FOUNDINGFREE. Info at pciai dot org."),
 ]),
 'v5': (52.00, [
   ('b1', 0.00, "A model wrote the forecast. A person signs it. The skill that matters has moved."),
   ('b2', 5.80, "So this institute exists for that judgement. Three credentials: controls, finance, and delivery."),
   ('b3', 11.80, "Behind all three, one body of knowledge. Thirteen domains, assessed, then publicly verifiable."),
   ('b4', 17.60, "Why is there a founding offer? Because it is early. For that reason, and no other."),
   ('b5', 23.60, "That is a fact about a stage. It is not a claim about what the work is worth."),
   ('b6', 29.40, "And to be plain. No countdown. No last places. We will not invent a deadline."),
   ('b7', 35.20, "Founding enrolment is free. Apply FOUNDINGFREE — membership, study access and exam enrolment, on a PCI account."),
   ('b8', 41.80, "Three steps, not one click. Create an account. Sign in. Apply the code."),
   ('b9', 47.20, "Questions first? Info at pciai dot org."),
 ]),
}

if __name__ == '__main__':
    WPS = 2.3
    print(f"{'film':5} {'beat':5} {'slot':>6} {'budget':>7} {'words':>6}  fit")
    over = 0
    for film, (dur, beats) in SCRIPTS.items():
        for i, (bid, start, text) in enumerate(beats):
            end = beats[i+1][1] if i+1 < len(beats) else dur
            slot = end - start
            words = len(text.split())
            need = words / WPS
            ok = need <= slot - 0.15
            if not ok: over += 1
            print(f"{film:5} {bid:5} {slot:6.2f} {slot*WPS:7.1f} {words:6d}  {'ok' if ok else 'OVER by %.1fs' % (need-slot)}")
    print("\nbeats over budget:", over)

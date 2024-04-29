import string

def z_array(s):
  """ Use Z algorithm (Gusfield Theorem 1.4.1) to preprocess string"""
  assert len(s) > 1
  z = [len(s)] + [0] * (len(s) - 1)

  # Initial Comparison of string[1:] with prefix
  for i in range (1, len(s)):
    if s[i] == z[i - 1]:
      z[1] += 1
    else:
      break

  r, l = 0, 0
  if z[1] > 0:
    r, l = z[1], 1

  for k in range(2, len(s)):
    assert z[k] == 0
    if k > r:
      # Case 1
      for i in range(k, len(s)):
        if s[i] == s[i - k]:
          z[k] += 1
        else:
          break
      r, l = k + z[k] - 1, k
    else:
      # Case 2
      # Calculate length of beta
      nbeta = r - k + 1
      zkp = z[k - 1]
      if nbeta > zkp:
        # Case 2a: Zkp wins
        z[k] = zkp
      else:
        # Case 2b: Compare characters just past r
        nmatch = 0
        for i in range(r + 1, len(s)):
          if s[i] == s[i -k]:
            nmatch += 1
          else:
            break
        l, r = k, r + nmatch
        z[k] = r - k + 1
  return z

def n_array(s):
  """ Compile L array (Gusfield Theorem 2.2.2) from the Z array """
  return z_array(s[::-1])[::-1]

def big_l_prime_array(p, n):
  """ Compile L' array (Gusfield theorem 2.2.2) using p and N array.
      L [i] = largest index j less than n such that N[j] = |P[1:]| """

  lp = [0] * len(p)
  for j in range(len(p) - 1):
    i = len(p) - n[j]
    if i < len(p):
      lp[i] = j + 1
  return lp

def big_l_array (p, lp):
  """ Compile L array (Gusfield theorem 2.2.2) using p and L array.
      L [i] = largets index j less than n such that N[j] >= |P[1:]| """
  l = [0] * len(p)
  l[1] = lp[1]
  for i in range(2, len(p)):
    l[i] = max(l[i-1], lp[i])
  return l

def small_l_prime_array(n):
  """ Comple lp array (Gusfield Theorem 2.2.4) using N array. """
  small_lp = [0] * len(n)
  for i in range(len(n)):
    if n[i] == i + 1: # prefix matching a suffix
      small_lp[len(n) - i -1] = i + 1
  for i in range(len(n) - 2, -1, -1): # smear them out to the left
    if small_lp[i] == 0:
      small_lp[i] = small_lp[i+1]
  return small_lp

def good_suffix_table(p):
  """ Return tables needed to apply good suffix rule. """
  n = n_array(p)
  lp = big_l_prime_array(p, n)
  return lp, big_l_array(p, lp), small_l_prime_array(n)

def good_suffix_mismatch(i, big_l_prime, small_l_prime):
  """ Given a mismatch at offset i, and given L/L' and l' arrays, return amount to shift
      as determined by good suffix rule. """

  length = len(big_l_prime)
  assert i < length
  if i == length - 1:
    return 0

  i += 1
  if big_l_prime[i] > 0:
    return length - big_l_prime[i]
  return length - small_l_prime[i]

def good_suffix_match(small_l_prime):
  """ Given a full match of P to T, return amount to shift as
      determined by good suffix rule"""

  return len(small_l_prime) - small_l_prime[1]

def dense_bad_char_tab(p, amap):
  """ Given pattern string and list with ordered alphabet characters, create
      and return a dense bad character table. Table is indexed by offset
      then by character. """

  tab = []
  nxt = [0] * len(amap)
  for i in range(0, len(p)):
    c = p[i]
    assert c in amap
    tab.append(nxt[:])
    nxt[amap[c]] = i + 1
  return tab

def boyer_moore(p, p_bm, t, n = 1):
  i = 0
  
  occurences = []
  while (i < len(t) - len(p) + 1) and n > 0:
    shift = 1
    mismatched = False
    for j in range(len(p)-1, -1, -1):
      if not p[j] == t[i+j]:
        skip_bc = p_bm.bad_character_rule(j, t[i+j])
        skip_gs = p_bm.good_suffix_rule(j)
        shift = max(shift, skip_bc, skip_gs)
        mismatched = True
        break
    if not mismatched:
      occurences.append(i)
      skip_gs = p_bm.match_skip()
      shift = max(shift, skip_gs)
      n -= 1
    i += shift
    blank_space = " " * i
    new_string = blank_space + p
    print(t)
    print(new_string)
  return occurences

class BoyerMoore(object):
  """ Encapsulate pattern and associated Boyer-Moore preprocessing. """

  def __init__(self, p, alphabet = ''.join(chr(i) for i in range(0x0000, 0xFFFF))):
    self.p = p
    self.alphabet = alphabet

    # Create map from alphabet characters to integers
    self.amap = {}

    for i in range(len(self.alphabet)):
      self.amap[self.alphabet[i]] = i
    print(self.amap)
    # Make bad character rule table
    self.bad_char = dense_bad_char_tab(p, self.amap)

    # Create a Good suffix rule table
    _, self.big_l, self.small_l_prime = good_suffix_table(p)


  def bad_character_rule(self, i, c):
    """ Return # of skips given by bad character rule at off set i """
    assert c in self.amap
    ci = self.amap[c]
    assert i > (self.bad_char[i][ci]-1)
    return i - (self.bad_char[i][ci]-1)

  def good_suffix_rule(self, i):
    """ Given a mismatch at offset im return amount to shift
          as determined by (weak) good suffix rule. """

    length = len(self.big_l)
    assert i < length
    if i == length - 1:
      return 0

    i += 1 # i points to leftmost matching position of P

    if self.big_l[i] > 0:
      return length - self.big_l[i]
    return length - self.small_l_prime[i]

  def match_skip(self):
    """ Return amount to shift in case where P matches T """
    return len(self.small_l_prime) - self.small_l_prime[1]
  
def main():
  t ='One morning in December the steamer Tabo was laboriously ascending the tortuous course of the Pasig, carrying a large crowd of passengers toward the province of La Laguna. She was a heavily built steamer, almost round, like the tabú from which she derived her name, quite dirty in spite of her pretensions to whiteness, majestic and grave from her leisurely motion. Altogether, she was held in great affection in that region, perhaps from her Tagalog name, or from the fact that she bore the characteristic impress of things in the country, representing something like a triumph over progress, a steamer that was not a steamer at all, an organism, stolid, imperfect yet unimpeachable, which, when it wished to pose as being rankly progressive, proudly contented itself with putting on a fresh coat of paint. Indeed, the happy steamer was genuinely Filipino! If a person were only reasonably considerate, she might even have been taken for the Ship of State, constructed, as she had been, under the inspection of Reverendos and Ilustrísimos.… Bathed in the sunlight of a morning that made the waters of the river sparkle and the breezes rustle in the bending bamboo on its banks, there she goes with her white silhouette throwing out great clouds of smoke—the Ship of State, so the joke runs, also has the vice of smoking! The whistle shrieks at every moment, hoarse and commanding like a tyrant who would rule by shouting, so that no one on [2]board can hear his own thoughts. She menaces everything she meets: now she looks as though she would grind to bits the salambaw, insecure fishing apparatus which in their movements resemble skeletons of giants saluting an antediluvian tortoise; now she speeds straight toward the clumps of bamboo or against the amphibian structures, karihan, or wayside lunch-stands, which, amid gumamelas and other flowers, look like indecisive bathers who with their feet already in the water cannot bring themselves to make the final plunge; at times, following a sort of channel marked out in the river by tree-trunks, she moves along with a satisfied air, except when a sudden shock disturbs the passengers and throws them off their balance, all the result of a collision with a sand-bar which no one dreamed was there. Moreover, if the comparison with the Ship of State is not yet complete, note the arrangement of the passengers. On the lower deck appear brown faces and black heads, types of Indians,1 Chinese, and mestizos, wedged in between bales of merchandise and boxes, while there on the upper deck, beneath an awning that protects them from the sun, are seated in comfortable chairs a few passengers dressed in the fashion of Europeans, friars, and government clerks, each with his puro cigar, and gazing at the landscape apparently without heeding the efforts of the captain and the sailors to overcome the obstacles in the river. The captain was a man of kindly aspect, well along in years, an old sailor who in his youth had plunged into far vaster seas, but who now in his age had to exercise much greater attention, care, and vigilance to avoid dangers of a trivial character. And they were the same for each day: the same sand-bars, the same hulk of unwieldy steamer wedged into the same curves, like a corpulent dame [3]in a jammed throng. So, at each moment, the good man had to stop, to back up, to go forward at half speed, sending—now to port, now to starboard—the five sailors equipped with long bamboo poles to give force to the turn the rudder had suggested. He was like a veteran who, after leading men through hazardous campaigns, had in his age become the tutor of a capricious, disobedient, and lazy boy. Doña Victorina, the only lady seated in the European group, could say whether the Tabo was not lazy, disobedient, and capricious—Doña Victorina, who, nervous as ever, was hurling invectives against the cascos, bankas, rafts of coconuts, the Indians paddling about, and even the washerwomen and bathers, who fretted her with their mirth and chatter. Yes, the Tabo would move along very well if there were no Indians in the river, no Indians in the country, yes, if there were not a single Indian in the world—regardless of the fact that the helmsmen were Indians, the sailors Indians, Indians the engineers, Indians ninety-nine per cent, of the passengers, and she herself also an Indian if the rouge were scratched off and her pretentious gown removed. That morning Doña Victorina was more irritated than usual because the members of the group took very little notice of her, reason for which was not lacking; for just consider—there could be found three friars, convinced that the world would move backwards the very day they should take a single step to the right; an indefatigable Don Custodio who was sleeping peacefully, satisfied with his projects; a prolific writer like Ben-Zayb (anagram of Ibañez), who believed that the people of Manila thought because he, Ben-Zayb, was a thinker; a canon like Padre Irene, who added luster to the clergy with his rubicund face, carefully shaven, from which towered a beautiful Jewish nose, and his silken cassock of neat cut and small buttons; and a wealthy jeweler like Simoun, who was reputed to be the adviser and inspirer of all the acts of his Excellency, the Captain-General—[4]just consider the presence there of these pillars sine quibus non of the country, seated there in agreeable discourse, showing little sympathy for a renegade Filipina who dyed her hair red! Now wasn’t this enough to exhaust the patience of a female Job—a sobriquet Doña Victorina always applied to herself when put out with any one! The ill-humor of the señora increased every time the captain shouted “Port,” “Starboard” to the sailors, who then hastily seized their poles and thrust them against the banks, thus with the strength of their legs and shoulders preventing the steamer from shoving its hull ashore at that particular point. Seen under these circumstances the Ship of State might be said to have been converted from a tortoise into a crab every time any danger threatened. “But, captain, why don’t your stupid steersmen go in that direction?” asked the lady with great indignation. “Because it’s very shallow in the other, señora,” answered the captain, deliberately, slowly winking one eye, a little habit which he had cultivated as if to say to his words on their way out, “Slowly, slowly!” “Half speed! Botheration, half speed!” protested Doña Victorina disdainfully. “Why not full?” “Because we should then be traveling over those ricefields, señora,” replied the imperturbable captain, pursing his lips to indicate the cultivated fields and indulging in two circumspect winks. This Doña Victorina was well known in the country for her caprices and extravagances. She was often seen in society, where she was tolerated whenever she appeared in the company of her niece, Paulita Gomez, a very beautiful and wealthy orphan, to whom she was a kind of guardian. At a rather advanced age she had married a poor wretch named Don Tiburcio de Espadaña, and at the time we now see her, carried upon herself fifteen years of wedded life, false frizzes, and a half-European costume—for her whole ambition had been to Europeanize herself, with the result that from the ill-omened day of her wedding she had gradually, [5]thanks to her criminal attempts, succeeded in so transforming herself that at the present time Quatrefages and Virchow together could not have told where to classify her among the known races. Her husband, who had borne all her impositions with the resignation of a fakir through so many years of married life, at last on one luckless day had had his bad half-hour and administered to her a superb whack with his crutch. The surprise of Madam Job at such an inconsistency of character made her insensible to the immediate effects, and only after she had recovered from her astonishment and her husband had fled did she take notice of the pain, then remaining in bed  for several , to the great delight of Paulita, who was very fond of joking and laughing at her aunt. As for her husband, horrified at the impiety of what appeared to him to be a terrific parricide, he took to flight, pursued by the matrimonial furies (two curs and a parrot), with all the speed his lameness permitted, climbed into the first carriage he encountered, jumped into the first banka he saw on the river, and, a Philippine Ulysses, began to wander from town to town, from province to province, from island to island, pursued and persecuted by his bespectacled Calypso, who bored every one that had the misfortune to travel in her company. She had received a report of his being in the province of La Laguna, concealed in one of the towns, so thither she was bound to seduce him back with her dyed frizzes. Her fellow travelers had taken measures of defense by keeping up among themselves a lively conversation on any topic whatsoever. At that moment the windings and turnings of the river led them to talk about straightening the channel and, as a matter of course, about the port works. Ben-Zayb, the journalist with the countenance of a friar, was disputing with a young friar who in turn had the countenance of an artilleryman. Both were shouting, gesticulating, waving their arms, spreading out their hands, [6]stamping their feet, talking of levels, fish-corrals, the San Mateo River,2 of cascos, of Indians, and so on, to the great satisfaction of their listeners and the undisguised disgust of an elderly Franciscan, remarkably thin and withered, and a handsome Dominican about whose lips flitted constantly a scornful smile. The thin Franciscan, understanding the Dominican’s smile, decided to intervene and stop the argument. He was undoubtedly respected, for with a wave of his hand he cut short the speech of both at the moment when the friar-artilleryman was talking about experience and the journalist-friar about scientists. “Scientists, Ben-Zayb—do you know what they are?” asked the Franciscan in a hollow voice, scarcely stirring in his seat and making only a faint gesture with his skinny hand. “Here you have in the province a bridge, constructed by a brother of ours, which was not completed because the scientists, relying on their theories, condemned it as weak and scarcely safe—yet look, it is the bridge that has withstood all the floods and earthquakes!”3 “That’s it, puñales, that very thing, that was exactly what I was going to say!” exclaimed the friar-artilleryman, thumping his fists down on the arms of his bamboo chair. “That’s it, that bridge and the scientists! That was just what I was going to mention, Padre Salvi—puñales!” Ben-Zayb remained silent, half smiling, either out of respect or because he really did not know what to reply, and yet his was the only thinking head in the Philippines! Padre Irene nodded his approval as he rubbed his long nose. Padre Salvi, the thin and withered cleric, appeared to be satisfied with such submissiveness and went on in the [7]midst of the silence: “But this does not mean that you may not be as near right as Padre Camorra” (the friar-artilleryman). “The trouble is in the lake—” “The fact is there isn’t a single decent lake in this country,” interrupted Doña Victorina, highly indignant, and getting ready for a return to the assault upon the citadel. The besieged gazed at one another in terror, but with the promptitude of a general, the jeweler Simoun rushed in to the rescue. “The remedy is very simple,” he said in a strange accent, a mixture of English and South American. “And I really don’t understand why it hasn’t occurred to somebody.” All turned to give him careful attention, even the Dominican. The jeweler was a tall, meager, nervous man, very dark, dressed in the English fashion and wearing a pith helmet. Remarkable about him was his long white hair contrasted with a sparse black beard, indicating a mestizo origin. To avoid the glare of the sun he wore constantly a pair of enormous blue goggles, which completely hid his eyes and a portion of his cheeks, thus giving him the aspect of a blind or weak-sighted person. He was standing with his legs apart as if to maintain his balance, with his hands thrust into the pockets of his coat. “The remedy is very simple,” he repeated, “and wouldn’t cost a cuarto.” The attention now redoubled, for it was whispered in Manila that this man controlled the Captain-General, and all saw the remedy in process of execution. Even Don Custodio himself turned to listen. “Dig a canal straight from the source to the mouth of the river, passing through Manila; that is, make a new river-channel and fill up the old Pasig. That would save land, shorten communication, and prevent the formation of sandbars.” The project left all his hearers astounded, accustomed as they were to palliative measures. [8] “It’s a Yankee plan!” observed Ben-Zayb, to ingratiate himself with Simoun, who had spent a long time in North America. All considered the plan wonderful and so indicated by the movements of their heads. Only Don Custodio, the liberal Don Custodio, owing to his independent position and his high offices, thought it his duty to attack a project that did not emanate from himself—that was a usurpation! He coughed, stroked the ends of his mustache, and with a voice as important as though he were at a formal session of the Ayuntamiento, said, “Excuse me, Señor Simoun, my respected friend, if I should say that I am not of your opinion. It would cost a great deal of money and might perhaps destroy some towns.” “Then destroy them!” rejoined Simoun coldly. “And the money to pay the laborers?” “Don’t pay them! Use the prisoners and convicts!” “But there aren’t enough, Señor Simoun!” “Then, if there aren’t enough, let all the villagers, the old men, the youths, the boys, work. Instead of the fifteen days of obligatory service, let them work three, four, five months for the State, with the additional obligation that each one provide his own food and tools.”The startled Don Custodio turned his head to see if there was any Indian within ear-shot, but fortunately those nearby were rustics, and the two helmsmen seemed to be very much occupied with the windings of the river. “But, Señor Simoun—” "Don’t fool yourself, Don Custodio,” continued Simoun dryly, “only in this way are great enterprises carried out with small means. Thus were constructed the Pyramids, Lake Moeris, and the Colosseum in Rome. Entire provinces came in from the desert, bringing their tubers to feed on. Old men, youths, and boys labored in transporting stones, hewing them, and carrying them on their shoulders under the direction of the official lash, and afterwards, the survivors returned to their homes or perished [9]in the sands of the desert. Then came other provinces, then others, succeeding one another in the work during years. Thus the task was finished, and now we admire them, we travel, we go to Egypt and to Home, we extol the Pharaohs and the Antonines. Don’t fool yourself—the dead remain dead, and might only is considered right by posterity.” “But, Señor Simoun, such measures might provoke uprisings,” objected Don Custodio, rather uneasy over the turn the affair had taken. “Uprisings, ha, ha! Did the Egyptian people ever rebel, I wonder? Did the Jewish prisoners rebel against the pious Titus? Man, I thought you were better informed in history!” Clearly Simoun was either very presumptuous or disregarded conventionalities! To say to Don Custodio’s face that he did not know history! It was enough to make any one lose his temper! So it seemed, for Don Custodio forgot himself and retorted, “But the fact is that you’re not among Egyptians or Jews!” “And these people have rebelled more than once,” added the Dominican, somewhat timidly. “In the times when they were forced to transport heavy timbers for the construction of ships, if it hadn’t been for the clerics—”'
  p = 'One'
  p_bm = BoyerMoore(p)
  n = 2
  print(boyer_moore(p, p_bm,t, n))


if __name__ == "__main__":
  main()
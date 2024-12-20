import unittest
from CodeParser import ByondParser
from wikiparser import WikiParser

class Tests(unittest.TestCase):
    def test_simple(self):
        code = '''
/something/type/class
\tname = "Test"

'''
        parser = ByondParser()
        classes = parser.parse(code).classes
        self.assertIsNotNone(classes)
        self.assertTrue(len(classes) == 1)
        self.assertTrue(classes[0].properties["name"] == "Test")

    def test_simple_value(self):
        code = '''
/something/type/class
\tvalue = 10 * 100

'''
        parser = ByondParser()
        classes = parser.parse(code).classes
        self.assertIsNotNone(classes)
        self.assertTrue(len(classes) == 1)
        self.assertTrue(classes[0].properties["value"] == "10 * 100")

    def test_inline_comment_class(self):
        code = '''
/something/type/class // This is a comment
\tname = "Test"

'''
        parser = ByondParser()
        classes = parser.parse(code).classes
        self.assertIsNotNone(classes)
        self.assertTrue(len(classes) == 1)
        self.assertTrue(classes[0].properties["name"] == "Test")

    def test_inline_comment_property(self):
        code = '''
/something/type/class
\tname = "Test" // This is another comment

'''
        parser = ByondParser()
        classes = parser.parse(code).classes
        self.assertIsNotNone(classes)
        self.assertTrue(len(classes) == 1)
        self.assertTrue(classes[0].properties["name"] == "Test")

    def test_method(self):
        code = '''
/something/type/class
\tname = "Test"

/something/type/class/method()
\tcode_line_a = 0
\tcode_line_b = 1

'''
        parser = ByondParser()
        classes = parser.parse(code).classes
        self.assertEqual(len(classes), 1)
        self.assertEqual(len(classes[0].methods), 1)
        self.assertEqual(classes[0].methods[0].name, "method")
        self.assertEqual(classes[0].methods[0].code, "\tcode_line_a = 0\n\tcode_line_b = 1\n")

    def test_method_line_in_code(self):
        code = '''
/something/type/class
\tname = "Test"

/something/type/class/method()
\tcode_line_a = 0

\tcode_line_b = 1

'''
        parser = ByondParser()
        classes = parser.parse(code).classes
        self.assertEqual(len(classes), 1)
        self.assertEqual(len(classes[0].methods), 1)
        self.assertEqual(classes[0].methods[0].name, "method")
        self.assertEqual(classes[0].methods[0].code, "\tcode_line_a = 0\n\n\tcode_line_b = 1\n")

    def test_method_with_comment(self):
        code = '''
/something/type/class
\tname = "Test"

/something/type/class/method() // this is a comment
\tcode_line_a = 0
\tcode_line_b = 1

'''
        parser = ByondParser()
        classes = parser.parse(code).classes
        self.assertEqual(len(classes), 1)
        self.assertEqual(len(classes[0].methods), 1)
        self.assertEqual(classes[0].methods[0].name, "method")
        self.assertEqual(classes[0].methods[0].code, "\tcode_line_a = 0\n\tcode_line_b = 1\n")

    def test_method_with_comment_and_params(self):
        code = '''
/something/type/class
\tname = "Test"

/something/type/class/method(var/something/a, var/something/b) // this is a comment
\tcode_line_a = 0
\tcode_line_b = 1

'''
        parser = ByondParser()
        classes = parser.parse(code).classes
        self.assertEqual(len(classes), 1)
        self.assertEqual(len(classes[0].methods), 1)
        self.assertEqual(classes[0].methods[0].name, "method")
        self.assertEqual(classes[0].methods[0].code, "\tcode_line_a = 0\n\tcode_line_b = 1\n")

    def test_global_proc(self):
        code = '''
/something/proc/method()
\tset name = "Test"

'''
        parser = ByondParser()
        procs = parser.parse(code).procs
        self.assertEqual(len(procs), 1)
        self.assertEqual(procs[0].name, "something/proc/method")
        self.assertEqual(procs[0].code, '\tset name = "Test"\n')

    def test_global_proc_underscore(self):
        code = '''
/mob/living/carbon/human/proc/psionic_swarm()
\tset category = "Psionic powers"
\tset name = "Psionic Swarm (2)"
\tset desc = "Spend two psionic essence to call forth a psionic energy cloud that will rip at foes and protect you for a short time."

'''
        parser = ByondParser()
        procs = parser.parse(code).procs
        self.assertEqual(len(procs), 1)
        self.assertEqual(procs[0].name, "mob/living/carbon/human/proc/psionic_swarm")
        self.assertEqual(procs[0].code, '\tset category = "Psionic powers"\n\tset name = "Psionic Swarm (2)"\n\tset desc = "Spend two psionic essence to call forth a psionic energy cloud that will rip at foes and protect you for a short time."\n')

    def test_global_proc_multilinestring(self):
        code = '''
/something/proc/method()
\tset name = "Testtext blabla \\
\tblablabla"

'''
        parser = ByondParser()
        procs = parser.parse(code).procs
        self.assertEqual(len(procs), 1)
        self.assertEqual(procs[0].name, "something/proc/method")
        self.assertEqual(procs[0].code, '\tset name = "Testtext blabla \\\n\tblablabla"\n')     

    def test_act_data(self):
        code='''
/datum/perk/codespeak
	name = "Codespeak"
	desc = "You know Marshal codes."
	icon_state = "codespeak" // https://game-icons.net/1x1/delapouite/police-officer-head.html
	var/list/codespeak_procs = list(
		/mob/living/carbon/human/proc/codespeak_help,
		/mob/living/carbon/human/proc/codespeak_clear,
		/mob/living/carbon/human/proc/codespeak_regroup,
		/mob/living/carbon/human/proc/codespeak_moving,
		/mob/living/carbon/human/proc/codespeak_moving_away,
		/mob/living/carbon/human/proc/codespeak_spooders,
		/mob/living/carbon/human/proc/codespeak_romch,
		/mob/living/carbon/human/proc/codespeak_bigspooders,
		/mob/living/carbon/human/proc/codespeak_bigromch,
		/mob/living/carbon/human/proc/codespeak_serb,
		/mob/living/carbon/human/proc/codespeak_commie,
		/mob/living/carbon/human/proc/codespeak_carrion,
		/mob/living/carbon/human/proc/codespeak_mutant,
		/mob/living/carbon/human/proc/codespeak_dead,
		/mob/living/carbon/human/proc/codespeak_corpse,
		/mob/living/carbon/human/proc/codespeak_criminal,
		/mob/living/carbon/human/proc/codespeak_unknown,
		/mob/living/carbon/human/proc/codespeak_status,
		/mob/living/carbon/human/proc/codespeak_detaining,
		/mob/living/carbon/human/proc/codespeak_shutup,
		/mob/living/carbon/human/proc/codespeak_understood,
		/mob/living/carbon/human/proc/codespeak_yes,
		/mob/living/carbon/human/proc/codespeak_no,
		/mob/living/carbon/human/proc/codespeak_detain_local,
		/mob/living/carbon/human/proc/codespeak_understood_local,
		/mob/living/carbon/human/proc/codespeak_yes_local,
		/mob/living/carbon/human/proc/codespeak_no_local,
		/mob/living/carbon/human/proc/codespeak_warcrime_local,
		/mob/living/carbon/human/proc/codespeak_rules_of_engagmentn_local,
		/mob/living/carbon/human/proc/codespeak_run_local
		)

/datum/perk/codespeak/assign(mob/living/L)
	..()
	if(holder)
		add_verb(holder, codespeak_procs)

/datum/perk/codespeak/remove()
	if(holder)
		remove_verb(holder, codespeak_procs)
	..()

/datum/perk/gunsmith
	name = "Gunsmith Master"
	desc = "You are a professional gunsmith, your knowledge allows to not only repair firearms but expertly craft them. \
			This includes the machines required to do so, including the bullet fabricator."
	icon_state = "gunsmith"

'''
        parser = ByondParser()
        classes = parser.parse(code).classes
        self.assertEqual(len(classes), 2)

if __name__ == "__main__":
    unittest.main()

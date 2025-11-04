#!/usr/bin/env python3
"""Test script for LLMClient."""

import os
import json
from app.clients.llm_client import LLMClient
from dotenv import load_dotenv

load_dotenv()

def test_llm_client():
    """Test LLMClient with sample vacancy text."""
    
    # Create output directory
    output_dir = "llm_test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY environment variable not set")
        print("Set it with: export GROQ_API_KEY='your_api_key_here'")
        return
    
    # Initialize client
    client = LLMClient(api_key=api_key)
    
    # Sample vacancy text
    sample_text = "Job als Werkstudent Data Quality (Inhouse) (m/w/d) Stellenanzeige Ähnliche Jobs Video Events Als Favorit einfügen Jetzt bewerben Zurück zur Suche | Corporate Functions Werkstudent Data Quality (Inhouse) (m/w/d) Du willst im Bereich Corporate Functions Risk & Reputation ein bedarfsgerechtes Risiko- und Compliance Management umsetzen? Unser Team setzt sich mit vielfältigen und innovativen Maßnahmen dafür ein, die fachliche Qualität im Einklang mit den regulatorischen Anforderungen zu sichern. Sichere unseren gemeinsamen Erfolg und mach mit uns den Unterschied: als Werkstudent Data Quality (m/w/d). Standorte: Düsseldorf, Berlin, Frankfurt, Hamburg, Hannover, Köln, Leipzig, München, Nürnberg und Stuttgart. Dein Impact: Als Werkstudent Data Quality (m/w/d) konzentrierst du dich auf die Bearbeitung von Kunden- und Auftragsdaten. Hier unterstützt du unser Team Client Acceptance & Conflicts , ergänzende Informationen zu ermitteln und zu prüfen. Das Ziel: die Qualität unserer fachlichen Arbeit zu sichern und die regulatorischen Anforderungen einzuhalten. Datenpflege: Auf Data Quality liegt unser gemeinsamer Fokus. Hand in Hand mit den verantwortlichen Bereichen bereitest du nach rechtlichen und internen Anforderungen relevante Daten auf. Tagesgeschäft: Ein wesentlicher Aspekt deines Joballtags ist es, Unternehmensinformationen gewissenhaft zu recherchieren. Data Management: In unserem internen System Salesforces pflegst du Daten ein und stellst dabei unseren Anspruch an eine hohe Qualität der Daten jederzeit sicher. Prozessoptimierung & Wissenstransfer: Gerne binden wir dich auch als Sparringspartner:in für den Team Lead bei der Entwicklung, Definition und Implementierung manueller und systemgestützter Prozesse ein. Dein Skillset: Student:in der Wirtschaftswissenschaften oder einer vergleichbaren Fachrichtung mit mindestens zwei Semestern Reststudienzeit Optimalerweise erste Erfahrungen in Research oder Data Quality Management Sichere Kenntnisse in Datenbankenrecherche und Internetnutzung als Informationsquelle, gepaart mit sicheren MS-Office-Skills Spaß an Teamarbeit, im Umgang mit Kolleg:innen agierst du offen und kommunikativ Deutsch und Englisch sehr gut in Wort und Schrift Deine Chance: Echte Verantwortung für eigene Aufgabenpakete innerhalb unserer Projekte, die du selbständig bearbeitest Persönliche:r Mentor:in in deinem Team, der/die dir mit Rat und Tat zur Seite steht und dich mit umfassendem Know-how unterstützt Ein chancenreiches und internationales Umfeld , das dir einmalige Einblicke in die Arbeit des weltweit größten Prüfungs- und Beratungsunternehmens bietet Work-Life-Balance in einem innovativen Unternehmensumfeld, das dir Gesundheitstage, Mitarbeiter:innen-Events und vieles mehr bietet Bereichsübergreifendes Networking im Deloitte Student Network mit exklusiven Vorträgen und regelmäßigem Austausch beim Praktikant:innen-Stammtisch Vielfältige Gestaltungsspielräume und aktive Förderung einer inklusiven Unternehmenskultur u. a. durch unsere Diversity & Inclusion Mitarbeiter:innen-Netzwerke Wann du verfügbar sein solltest Als Werkstudent:in bist du ab sofort für mindestens ein Jahr an bis zu 20 Stunden pro Woche für uns tätig, wobei deine Arbeitszeit flexibel gestaltet werden kann. In der vorlesungsfreien Zeit ist eine Erhöhung deiner Wochenarbeitszeit auf bis zu 40 Stunden pro Woche möglich. Es besteht die Möglichkeit des Remote Workings nach der Einarbeitungszeit. Bist du bereit? Mach mit uns den Unterschied! Unser Recruiting-Team freut sich auf deine Bewerbungsunterlagen (CV sowie Abitur-, Hochschul- und Arbeitszeugnisse) über unser Online-Formular. Ein Anschreiben und ein Bewerbungsfoto sind bei uns nicht erforderlich. Job Visitenkarte Werkstudent Data Quality (Inhouse) (m/w/d) JOB-ID: 41801 STANDORT Berlin, Düsseldorf, Frankfurt (Main), Köln, Leipzig, Hamburg, Hannover, München, Nürnberg, Stuttgart JOBART Studentische Aushilfe KEYWORDS Student:innen Corporate Functions R&R Client Acceptance & Continuance AI & Data Analytics GESCHÄFTSBEREICH Lerne den Geschäftsbereich Corporate Functions kennen. ZIELGRUPPE Finde heraus, welche Möglichkeiten wir für Student:innen bieten. DIESEN JOB TEILEN Gleiche Chancen für alle: Wir freuen uns über Bewerbungen von Menschen, die so vielfältig sind wie wir unabhängig von Alter, Behinderung, ethnischer Herkunft und Nationalität, Geschlecht, Religion, sexueller Orientierung oder sozialer Herkunft. Noch Fragen? Alle Infos zu unserem Bewerbungsprozess findest du in unseren Bewerbungs-FAQs. Bewerbungsfrist: Solange der Job angezeigt wird, kannst du dich schnell und bequem online bewerben. Jobs werden häufig an verschiedenen Standorten mehrfach besetzt und du kannst flexibel jeden Monat beginnen - sofern nicht im Stellentext genannt, gibt es keinen Bewerbungsschluss. Internationales Arbeitsumfeld Mehr lesen Unser internationales Netzwerk vereint das Know-how von rund 457.000 Mitarbeitenden aus über 150 Ländern. Wir stehen für weltweite Kompetenz, für Vertrauen, Innovation und starken Zusammenhalt. Weiterbildungs-Programme Mehr lesen Wir investieren besonders viel in die Weiterbildung und systematische Entwicklung der Skills und Schlüsselqualifikationen unserer Mitarbeitenden, damit sie zu den Besten auf ihrem Gebiet gehören. Kollegiale Arbeitsatmosphäre Mehr lesen Wir setzen uns für eine offene Unternehmenskultur ein, die Vielfalt und Vertrauen fördert. Kollegialität sowie Integrität steht an oberster Stelle und der Deloitte Team-Spirit wird aktiv gefördert. Remote Work Mehr lesen Wir möchten das Arbeiten bei Deloitte so attraktiv und flexibel wie möglich gestalten. Deshalb ermöglichen wir es, von überall aus in Deutschland sowie unter Einhaltung bestimmter Richtlinien auch aus verschiedenen (EU-)Ländern heraus zu arbeiten. Job Matching Du bist dir nicht sicher, ob die Stelle zu dir passt? Finde es heraus: Lade deinen Lebenslauf hoch und lass dir passende Stellen vorschlagen. Nutze unser Job Matching Gemeinsam zum Ziel Wir suchen engagierte Fachleute mit Leidenschaft für ihren Beruf und dem Ehrgeiz, sich weiterzuentwickeln. Mithilfe der folgenden Schritte versuchen wir, so viel wie möglich über dich und deine Kenntnisse und Fähigkeiten herauszufinden. Der Personalverantwortliche wird dich durch diesen Prozess leiten. Wir freuen uns auf deine Bewerbung. Bei Deloitte heißen wir jede:n willkommen, der Qualität und Ehrgeiz mitbringt. Unser Bewerbungsprozess Wir verraten dir, wie du dich am besten vorbereiten und was du bei deiner Bewerbung beachten solltest. Erfahre hier mehr Du hast noch Fragen? Hier findest du unsere Bewerbungs-FAQs, in denen häufig gestellte Fragen direkt beantwortet werden. Bewerbungs-FAQs Ähnliche Jobs Zuletzt angesehene Jobs Deine Favoriten Unsere Auswahl aus 6 Jobs für dich Werkstudent im Bereich Corporate Security / IT-Sicherheit (m/w/d) Düsseldorf Student:innen Corporate Functions R&R Information Security Werkstudent Geldwäschebekämpfung (Inhouse) (m/w/d) Düsseldorf Student:innen Corporate Functions R&R Independence Werkstudent Talent Acquisition (m/w/d) Leipzig, Düsseldorf, Frankfurt (Main) Student:innen Corporate Functions People - Attraction Werkstudent Economic Research (m/w/d) München Student:innen Corporate Functions Insights & Knowledge Werkstudent Finance & Accounting (Inhouse) - Jahresabschluss (m/w/d) Düsseldorf Student:innen Corporate Functions Finance & Accounting Accounting / IFRS Werkstudent Operational Excellence & Digitalization (OED) (w/m/d) Düsseldorf Student:innen Corporate Functions Business Services Center alle Jobs zeigen A career built around you Was dich im Bereich Corporate Functions erwartet Dafür sorgen, dass alle Kerngeschäftsprozesse reibungslos funktionieren dafür stehen die Corporate Functions bei Deloitte. Die Teams unterstützen die Geschäftsführung sowie Businesses gezielt in allen Geschäftsprozessen. \"Ich habe das Gefühl, dass ich mit meiner Arbeit wirklich etwas vorantreiben und einen Mehrwert im Unternehmen generieren kann das ist ein unglaublich erfüllendes Gefühl!\" Tammi HR Advisory Associate Manager \"Die eigenen Interessen sind entscheidend bei der Berufswahl: Wofür schlägt euer Herz? Was motiviert euch, wo liegen eure persönlichen Stärken, Ziele und Erwartungen?\" Anja Corporate Functions Head of Talent Acquisition \"Als interne IT-Abteilung ist es unsere wichtigste Aufgabe, digitales Arbeiten bei Deloitte zu ermöglichen und das so effizient, sicher und zuverlässig wie möglich.\" Dajana Corporate Functions Head of Business Transformation Services DTech \"Wenn du die Frage, ob du ein Teamplayer bist mit Ja beantworten kannst, bist du genau richtig bei uns.\" Melanie Corporate Functions Backoffice Manager 19.000 Quadratmeter, eine Vision: aus vier Büros wird ein neuer zentraler Standort. Carolin aus dem Bereich Real Estate & Operations gestaltet bei Deloitte die Zukunft des Arbeitens aktiv mit. Erfahre, wie sie den Umzug ins neue Berliner Büro begleitet und wie sie im Change Management von der Zusammenarbeit mit verschiedenen Teams und Persönlichkeiten profitiert. 0:00 2:15 Carolin Real Estate & Operations Managerin Transkript Events bei Deloitte München HOKO - Hochschulkontaktmesse 2025 Event ansehen München meet@TUM School of Management Die Karrieremesse der TUM School of Managemen Event ansehen München LMU Karriereforum Event ansehen Leipzig Jobmesse WIK-Leipzig HTWK Event ansehen Karlsruhe bonding Karlsruhe 2025 Event ansehen Alle Events bei Deloitte Deutschlandweit Team Talent Acquisition Aleksandra, Lea, Anja, Julia, Silja, Lisa und ihre Teams stehen dir bei Fragen gerne zur Verfügung. Dein Kontakt bei Fragen rund um Karrierethemen Wir freuen uns, von dir zu hören! Bitte bewirb dich aus Datenschutzgründen ausschließlich über unser Online-Bewerbungssystem via des Buttons \"Jetzt bewerben\". Bewerbungen via E-Mail können wir leider nicht berücksichtigen. career@deloitte.de +49 211 87724111 Making an impact that matters. Deloitte bietet führende Prüfungs- und Beratungsleistungen in den Bereichen Audit & Assurance, Tax & Legal, Consulting und Advisory für nahezu 90% der Fortune Global 500 -Unternehmen und Tausende von privaten Unternehmen an. Wir liefern innovative Denkansätze, lösen komplexe Herausforderungen und ermöglichen nachhaltiges Wachstum. Gleichzeitig eröffnen wir hervorragende Karrierechancen für unsere rund 460.000 Mitarbeitenden weltweit. Ganz gleich, ob BWL oder MINT Diversity fördert Innovation durch unterschiedliche Sichtweisen und Charaktere. Die Zeiten, bei Deloitte einzusteigen, waren nie spannender. Mach mit uns den Unterschied! Entdecke weitere Jobs für Studierende Praktikum Praktikum BWL Praktikum Consulting Praktikum Controlling Praktikum Data Science Praktikum Finance Praktikum HR Praktikum IT Praktikum M&A Praktikum Marketing Praktikum SAP / Werkstudent SAP (m/w/d) Praktikum Steuerberatung Praktikum Wirtschaftsprüfung Werkstudium Werkstudent Bank (m/w/d) Werkstudent BWL (m/w/d) Werkstudent Consulting (m/w/d) Werkstudent Controlling (m/w/d) Werkstudent Data Science (m/w/d) Werkstudent Finance (m/w/d) Werkstudent HR (m/w/d) Werkstudent Steuern (m/w/d) Werkstudent Wirtschaftsprüfung (m/w/d) Unsere Top Trends Accounting Jobs Automotive Jobs Bank Jobs Cloud Jobs Cyber Security Jobs Data & Analytics Jobs Mathematiker Jobs (m/w/d) Mergers & Acquisition Jobs Restrukturierung Jobs Salesforce Jobs SAP Berater Jobs (m/w/d) Steuerberatung Jobs Sustainability Jobs Versicherung Jobs Wirtschaftsprüfer Jobs (m/w/d)"
    
    print("Testing LLM client...")
    print(f"Sample text length: {len(sample_text)} characters")
    
    try:
        # Generate timestamp for filenames
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("Testing LLM client with stats...")
        
        # Extract info using LLM with stats
        result_with_stats = client.extract_vacancy_info(sample_text, include_stats=True)
        result = result_with_stats["response"]
        stats = result_with_stats["stats"]
        
        print("\nLLM extraction successful!")
        print("\n--- Extracted Information ---")
        print(f"Company: {result.company_name}")
        print(f"Role: {result.role_title}")
        print(f"Grade: {result.job_grade}")
        print(f"Salary: {result.expected_salary}")
        print(f"Contact: {result.contact_person}")
        print(f"Requirements: {result.requirements}")
        
        print(f"\n--- API Stats ---")
        print(f"TOKENS: {stats['usage']['total_tokens']} total")
        print(f"  ├── Prompt: {stats['usage']['prompt_tokens']}")
        print(f"  └── Completion: {stats['usage']['completion_tokens']}")
        print(f"Execution time: {stats['timing']['execution_time_seconds']} seconds")
        print(f"Model: {stats['model']}")
        print(f"Request ID: {stats['id']}")
        
        # Save everything in one JSON file
        test_data = {
            "metadata": {
                "timestamp": timestamp,
                "success": True,
                "test_type": "llm_extraction"
            },
            "input": {
                "text_content": sample_text,
                "text_length": len(sample_text),
                "model_config": {
                    "model": client.model,
                    "temperature": client.temperature,
                    "max_tokens": client.max_tokens
                }
            },
            "output": {
                "extraction_result": result.model_dump()
            },
            "statistics": {
                "tokens": {
                    "prompt_tokens": stats['usage']['prompt_tokens'],
                    "completion_tokens": stats['usage']['completion_tokens'], 
                    "total_tokens": stats['usage']['total_tokens']
                },
                "timing": {
                    "execution_time_seconds": stats['timing']['execution_time_seconds'],
                    "start_time": stats['timing']['start_time'],
                    "end_time": stats['timing']['end_time']
                },
                "api_info": {
                    "model": stats['model'],
                    "created": stats['created'],
                    "id": stats['id'],
                    "system_fingerprint": stats['system_fingerprint']
                },
                "full_api_stats": stats
            }
        }
        
        output_file = f"{output_dir}/test_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        print(f"\nComplete test data saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        
        # Save error info in same format
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        test_data = {
            "metadata": {
                "timestamp": timestamp,
                "success": False,
                "test_type": "llm_extraction"
            },
            "input": {
                "text_content": sample_text,
                "text_length": len(sample_text),
                "model_config": {
                    "model": client.model,
                    "temperature": client.temperature,
                    "max_tokens": client.max_tokens
                }
            },
            "error": {
                "message": str(e),
                "traceback": traceback.format_exc()
            }
        }
        
        output_file = f"{output_dir}/test_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        print(f"Error test data saved to: {output_file}")


if __name__ == "__main__":
    test_llm_client()
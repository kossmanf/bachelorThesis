# bachelorThesis
Repository für die Bachelorarbeit zum Thema Goal-Directed Reasoning in First-Order Logic through Learning from Proofs Using Large Language Models an der Hochschule Trier

Erklärung der Ordner:

1. Categorize Goals:
Enthält Dateien zur Kategorisierung von Zielen aus AdimenSumo und ApplyingCWA.
categorize_goals.py: Diese Datei dient dazu, Ziele aus AdimenSUMO und ApplyingCWA zu kategorisieren.

2. Axiom Generation:
Enthält Dateien zur Generierung von Axiomen aus AdimenSumo für Beweise mit dem Eprover.
generateAxioms.py: Generiert Axiome, die für Beweise mit dem Eprover benötigt werden, indem die Axiome aus AdimenSumo mit Zielen kombiniert werden.

3. Generating Proofs:
Enthält Dateien zum Erbringen von Beweisen mithilfe des Eprovers.
generate_proofs.py: Dient dem Führen von Beweisen mittels der erstellten Axiom-Dateien mit dem Eprover. Voraussetzung ist eine installierte und funktionierende Version des Eprovers.

4. Processing Proofs:
Ordner enthält Dateien zur weiteren Verarbeitung von Beweisen.
separatedCompletedFromUncompletedProofs.py: Trennt erbrachte von nicht erbrachten Beweisen.
separateTestFromTrainingData.py: Trennt Beweise, die für die spätere Analyse, von den Beweisen, die für das Training des Sprachmodells verwendet werden sollen.

5. Mapping to Natural Language:
Dieser Ordner enthält eine Datei, die Adimen Sumo Symbole auf natürliche Sprache abbildet.
as_cn_mapping_test.json: Bildet Symbole aus Adimen Sumo auf natürliche Sprache ab.

6. TPTP Parser:
Dieser Ordner enthält Dateien zum Parsen von Formeln in TPTP-Syntax.
treeDataStructure.py: Datenstruktur für den Parse-Baum.
parseTree.py: Erstellt einen Parse-Baum für eine TPTP-Formel.
parseTreeExtraction.py: Ermöglicht das Extrahieren bestimmter Operatoren (Funktionssymbole, Konstantensymbole, Variablen, Konstanten) aus dem Parse-Baum.
printTree.py: Visualisiert den Parse-Baum.

7. Convert to Natural Language:
Dieser Ordner enthält eine Datei zum Umwandeln von Formeln in natürliche Sprache.
convertParseTreeToNaturalLanguage.py: Wandelt eine Formel in TPTP-Syntax über den Parse-Baum in natürliche Sprache um.

8. Generating Pre-training Data:
Dieser Ordner enthält Dateien zur Vorverarbeitung von Beweisen für die Generierung von Trainingsdaten.
generatePositiveAndNegativePreTrainingData.py: Trennt positive Trainingsdaten (die im Beweis vorkommen) von negativen Trainingsdaten (die nicht im Beweis vorkommen) und extrahiert Klauseln und Beweisziele aus den erbrachten Beweisen.
extractSymbolsFromPreTrainingData.py: Extrahiert Symbole aus den Klauseln und interpretiert sie als Dokumente, um später Trainingsdaten zu berechnen.
collectDocuments.py: Fasst die Dokumente in einer Datei zusammen für die spätere Berechnung von TF-IDF.
processPreTrainingData.py: Berechnet für jedes Symbol aus dem Wissensbasis für jeden erbrachten Beweis basierend auf diesen und allen anderen Beweisen einen Similarity Score für positive Symbole in Form von TF-IDF-Werten, für negative Symbole in Form von Häufigkeit und für neutrale Symbole den Wert 0.

9. generateTrainingTestDataForLM
In diesem Ordner befinden sich alle Dateien zur Erzeugung von Trainings- und Testdaten für das Sprachmodell.
generateTestAndTrainingData.py: Datei zur Erzeugung von Trainings- und Testdaten.

11. trainingDataLM
Dieser Ordner enthält alle Trainingsdaten für das Sprachmodell:
trainingDataK2.pt: Jeder Datensatz beinhaltet das Doppelte an negativen im Vergleich zu positiven Symbolen pro Beweis.
trainingDataK5.pt: Jeder Datensatz beinhaltet fünfmal mehr negative als positive Symbole pro Beweis.

12. testDataLM
Dieser Ordner umfasst alle Testdaten für das Sprachmodell:
testDataK2.pt: Für jeden Beweis enthält der Datensatz doppelt so viele negative wie positive Symbole.
testDataK5.pt: Für jeden Beweis enthält der Datensatz fünfmal mehr negative als positive Symbole.

13. training
Hier sind Dateien für das Training neuronaler Netze abgelegt.
training_cosineEmbeddingLoss.py: Datei für das Training mittels der Cosine Embedding Loss Funktion.
training_mseLoss.py: Datei für das Training mittels der Mean Squared Error Loss Funktion.

Hinweis: Es ist nicht sichergestellt, dass alle für ein Programm benötigten Dateien in den entsprechenden Ordnern liegen. Aus diesem Grund kann es zu Fehlern kommen beim Importieren oder Laden von Dateien.

# bachelorThesis
Repository for the bachelor thesis on Goal-Directed Reasoning in First-Order Logic through Learning from Proofs Using Large Language Models at Trier University of Applied Sciences

Explanation of the folders:

1. Categorize Goals:
Contains files for categorizing goals from AdimenSumo and ApplyingCWA.
categorize_goals.py: This file is used to categorize goals from AdimenSUMO and ApplyingCWA.

2. axiom generation:
Contains files for generating axioms from AdimenSumo for proofs with the eprover.
generateAxioms.py: Generates axioms needed for proofs with the eprover by combining the axioms from AdimenSumo with targets.

3. Generating Proofs:
Contains files for generating proofs using the eprover.
generate_proofs.py: Used to generate proofs using the generated axiom files with the Eprover. An installed and functioning version of the Eprover is required.

4. processing proofs:
Folder contains files for further processing of proofs.
separatedCompletedFromUncompletedProofs.py: Separates completed from uncompleted proofs.
separateTestFromTrainingData.py: Separates proofs that are to be used for later analysis from the proofs that are to be used for training the language model.

5. mapping to natural language:
This folder contains a file that maps Adimen Sumo symbols to natural language.
as_cn_mapping_test.json: Maps symbols from Adimen Sumo to natural language.

6. TPTP Parser:
This folder contains files for parsing formulas in TPTP syntax.
treeDataStructure.py: Data structure for the parse tree.
parseTree.py: Creates a parse tree for a TPTP formula.
parseTreeExtraction.py: Enables the extraction of certain operators (function symbols, constant symbols, variables, constants) from the parse tree.
printTree.py: Visualizes the parse tree.

7. Convert to Natural Language:
This folder contains a file for converting formulas to natural language.
convertParseTreeToNaturalLanguage.py: Converts a formula in TPTP syntax into natural language via the parse tree.

8. Generating Pre-training Data:
This folder contains files for pre-processing proofs to generate training data.
generatePositiveAndNegativePreTrainingData.py: Separates positive training data (clauses which appears in the proof) from negative training data ( clauses which does not appear in the proof) and extracts clauses and proof targets from the provided proofs.
extractSymbolsFromPreTrainingData.py: Extracts symbols from the clauses and interprets them as documents in order to calculate training data later.
collectDocuments.py: Collects the documents in a file for the later calculation of TF-IDF.
processPreTrainingData.py: Calculates the training data.
processPreTrainingData.py: Calculates a similarity score for each symbol from the knowledge base for each proof based on the proof and all other proofs in the form of TF-IDF values for positive symbols, in the form of frequency for negative symbols and the value 0 for neutral symbols.

9. generateTrainingTestDataForLM
This folder contains all the files for generating training and test data for the language model.
generateTestAndTrainingData.py: File for generating training and test data.

10. trainingDataLM
This folder contains all training data for the language model:
trainingDataK2.pt: Each data set contains twice as many negative symbols as positive symbols per proof.
trainingDataK5.pt: Each data set contains five times more negative than positive symbols per proof.

11. testDataLM
This folder contains all test data for the language model:
testDataK2.pt: For each proof, the data set contains twice as many negative symbols as positive symbols.
testDataK5.pt: For each proof, the data set contains five times as many negative symbols as positive symbols.

12. training
Files for training neural networks are stored here.
training_cosineEmbeddingLoss.py: File for training using the cosine embedding loss function.
training_mseLoss.py: File for training using the Mean Squared Error Loss function.

Note: It is not guaranteed that all files required for a program are located in the corresponding folders. For this reason, errors may occur when importing or loading files.
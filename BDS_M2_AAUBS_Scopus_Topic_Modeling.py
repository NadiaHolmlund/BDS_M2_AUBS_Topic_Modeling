{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyM3zeKXF/ye5xOn5BhF+wlb",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/NadiaHolmlund/BDS_M2_AAUBS_Scopus_Topic_Modeling/blob/main/BDS_M2_AAUBS_Scopus_Topic_Modeling.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Imports"
      ],
      "metadata": {
        "id": "thVuXFFlouyy"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install tweet-preprocessor -q\n",
        "!pip install -qq -U gensim\n",
        "!pip install -qq pyLDAvis"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "-_GbyalGsdeO",
        "outputId": "6c940d85-aaf6-4cac-c8e0-bd1fe39fed65"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\u001b[K     |████████████████████████████████| 24.1 MB 61.8 MB/s \n",
            "\u001b[K     |████████████████████████████████| 1.7 MB 8.5 MB/s \n",
            "\u001b[?25h  Installing build dependencies ... \u001b[?25l\u001b[?25hdone\n",
            "  Getting requirements to build wheel ... \u001b[?25l\u001b[?25hdone\n",
            "  Installing backend dependencies ... \u001b[?25l\u001b[?25hdone\n",
            "    Preparing wheel metadata ... \u001b[?25l\u001b[?25hdone\n",
            "  Building wheel for pyLDAvis (PEP 517) ... \u001b[?25l\u001b[?25hdone\n",
            "  Building wheel for sklearn (setup.py) ... \u001b[?25l\u001b[?25hdone\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "C9-VGdy-kX2u",
        "outputId": "41afac22-a769-4d75-dc13-e80bec461317"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "/usr/local/lib/python3.7/dist-packages/past/types/oldstr.py:5: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3,and in 3.9 it will stop working\n",
            "  from collections import Iterable\n",
            "/usr/local/lib/python3.7/dist-packages/past/builtins/misc.py:4: DeprecationWarning: Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated since Python 3.3,and in 3.9 it will stop working\n",
            "  from collections import Mapping\n"
          ]
        }
      ],
      "source": [
        "# Standard\n",
        "import pandas as pd\n",
        "import preprocessor as prepro\n",
        "import tqdm\n",
        "\n",
        "# Language preprocessing\n",
        "import spacy\n",
        "nlp = spacy.load('en_core_web_sm')\n",
        "\n",
        "# Topic modeling\n",
        "from gensim.corpora.dictionary import Dictionary # Import the dictionary builder\n",
        "from gensim.models import LdaMulticore # we'll use the faster multicore version of LDA\n",
        "\n",
        "# Topic Modeling Visualization\n",
        "import pyLDAvis\n",
        "import pyLDAvis.gensim_models as gensimvis"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Data Cleaning"
      ],
      "metadata": {
        "id": "uhhL9pa0ox4v"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "data = pd.read_csv('https://raw.githubusercontent.com/NadiaHolmlund/BDS_M2_AAUBS_Scopus_Topic_Modeling/main/Data/scopus.csv')"
      ],
      "metadata": {
        "id": "lr3Z-xiR-Smn"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "data.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "tr2M-BMh8Ijw",
        "outputId": "0639b3a2-1c14-42f9-be8e-566af5231fab"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(135, 20)"
            ]
          },
          "metadata": {},
          "execution_count": 4
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "data.head(5)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 676
        },
        "id": "El4CnKtVotkz",
        "outputId": "66215d6f-8f8d-496c-cd7e-5f98e1ec4db4"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "                                             Authors  \\\n",
              "0                    Gao Y., Hu Y., Liu X., Zhang H.   \n",
              "1  Xu X., Hu W., Liu W., Wang D., Huang Q., Huang...   \n",
              "2   Xu X., Hu W., Liu W., Wang D., Huang Q., Chen Z.   \n",
              "3           Saabye H., Kristensen T.B., Wæhrens B.V.   \n",
              "4             Crovini C., Ossola G., Britzelmaier B.   \n",
              "\n",
              "                                        Author(s) ID  \\\n",
              "0   57196280682;56580618100;35208483000;57169423400;   \n",
              "1  57205534107;24921323300;57193691954;5676303010...   \n",
              "2  57205534107;24921323300;57193691954;5676303010...   \n",
              "3               57219656715;57213084303;22837185500;   \n",
              "4                57200919718;6602427174;23471680600;   \n",
              "\n",
              "                                               Title  Year  \\\n",
              "0  Can Public R&D Subsidy Facilitate Firms’ Explo...  2021   \n",
              "1  Risk-based scheduling of an off-grid hybrid el...  2021   \n",
              "2  Study on the economic benefits of retired elec...  2021   \n",
              "3  Real-time data utilization barriers to improvi...  2020   \n",
              "4  How to reconsider risk management in SMEs? An ...  2021   \n",
              "\n",
              "                    Source title Volume Issue Art. No. Page start Page end  \\\n",
              "0                Research Policy     50     4   104221        NaN      NaN   \n",
              "1  Journal of Cleaner Production    315   NaN   128155        NaN      NaN   \n",
              "2  Journal of Cleaner Production    286   NaN   125414        NaN      NaN   \n",
              "3   Sustainability (Switzerland)     12    21     8757          1       21   \n",
              "4    European Management Journal     39     1      NaN        118      134   \n",
              "\n",
              "   Page count  Cited by                            DOI  \\\n",
              "0         NaN      27.0   10.1016/j.respol.2021.104221   \n",
              "1         NaN      11.0  10.1016/j.jclepro.2021.128155   \n",
              "2         NaN      10.0  10.1016/j.jclepro.2020.125414   \n",
              "3         NaN      10.0             10.3390/su12218757   \n",
              "4         NaN       9.0      10.1016/j.emj.2020.11.002   \n",
              "\n",
              "                                                Link  \\\n",
              "0  https://www.scopus.com/inward/record.uri?eid=2...   \n",
              "1  https://www.scopus.com/inward/record.uri?eid=2...   \n",
              "2  https://www.scopus.com/inward/record.uri?eid=2...   \n",
              "3  https://www.scopus.com/inward/record.uri?eid=2...   \n",
              "4  https://www.scopus.com/inward/record.uri?eid=2...   \n",
              "\n",
              "                                            Abstract Document Type  \\\n",
              "0  Public R&D subsidy is a commonly adopted polic...       Article   \n",
              "1  Making full use of renewable energy to supply ...       Article   \n",
              "2  The lithium-ion batteries of battery electric ...       Article   \n",
              "3  This study presents empirical evidence for the...       Article   \n",
              "4  The purpose of this paper is two-fold: to reco...       Article   \n",
              "\n",
              "  Publication Stage                   Open Access  Source                 EID  \n",
              "0             Final                           NaN  Scopus  2-s2.0-85101066073  \n",
              "1             Final                           NaN  Scopus  2-s2.0-85109437255  \n",
              "2             Final                           NaN  Scopus  2-s2.0-85097913846  \n",
              "3             Final  All Open Access, Gold, Green  Scopus  2-s2.0-85094607941  \n",
              "4             Final                           NaN  Scopus  2-s2.0-85096819200  "
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-0210e736-c9f9-4165-86b1-4540d7f4e3fa\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Authors</th>\n",
              "      <th>Author(s) ID</th>\n",
              "      <th>Title</th>\n",
              "      <th>Year</th>\n",
              "      <th>Source title</th>\n",
              "      <th>Volume</th>\n",
              "      <th>Issue</th>\n",
              "      <th>Art. No.</th>\n",
              "      <th>Page start</th>\n",
              "      <th>Page end</th>\n",
              "      <th>Page count</th>\n",
              "      <th>Cited by</th>\n",
              "      <th>DOI</th>\n",
              "      <th>Link</th>\n",
              "      <th>Abstract</th>\n",
              "      <th>Document Type</th>\n",
              "      <th>Publication Stage</th>\n",
              "      <th>Open Access</th>\n",
              "      <th>Source</th>\n",
              "      <th>EID</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Gao Y., Hu Y., Liu X., Zhang H.</td>\n",
              "      <td>57196280682;56580618100;35208483000;57169423400;</td>\n",
              "      <td>Can Public R&amp;D Subsidy Facilitate Firms’ Explo...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Research Policy</td>\n",
              "      <td>50</td>\n",
              "      <td>4</td>\n",
              "      <td>104221</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>27.0</td>\n",
              "      <td>10.1016/j.respol.2021.104221</td>\n",
              "      <td>https://www.scopus.com/inward/record.uri?eid=2...</td>\n",
              "      <td>Public R&amp;D subsidy is a commonly adopted polic...</td>\n",
              "      <td>Article</td>\n",
              "      <td>Final</td>\n",
              "      <td>NaN</td>\n",
              "      <td>Scopus</td>\n",
              "      <td>2-s2.0-85101066073</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>Xu X., Hu W., Liu W., Wang D., Huang Q., Huang...</td>\n",
              "      <td>57205534107;24921323300;57193691954;5676303010...</td>\n",
              "      <td>Risk-based scheduling of an off-grid hybrid el...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Journal of Cleaner Production</td>\n",
              "      <td>315</td>\n",
              "      <td>NaN</td>\n",
              "      <td>128155</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>11.0</td>\n",
              "      <td>10.1016/j.jclepro.2021.128155</td>\n",
              "      <td>https://www.scopus.com/inward/record.uri?eid=2...</td>\n",
              "      <td>Making full use of renewable energy to supply ...</td>\n",
              "      <td>Article</td>\n",
              "      <td>Final</td>\n",
              "      <td>NaN</td>\n",
              "      <td>Scopus</td>\n",
              "      <td>2-s2.0-85109437255</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Xu X., Hu W., Liu W., Wang D., Huang Q., Chen Z.</td>\n",
              "      <td>57205534107;24921323300;57193691954;5676303010...</td>\n",
              "      <td>Study on the economic benefits of retired elec...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Journal of Cleaner Production</td>\n",
              "      <td>286</td>\n",
              "      <td>NaN</td>\n",
              "      <td>125414</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>NaN</td>\n",
              "      <td>10.0</td>\n",
              "      <td>10.1016/j.jclepro.2020.125414</td>\n",
              "      <td>https://www.scopus.com/inward/record.uri?eid=2...</td>\n",
              "      <td>The lithium-ion batteries of battery electric ...</td>\n",
              "      <td>Article</td>\n",
              "      <td>Final</td>\n",
              "      <td>NaN</td>\n",
              "      <td>Scopus</td>\n",
              "      <td>2-s2.0-85097913846</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>Saabye H., Kristensen T.B., Wæhrens B.V.</td>\n",
              "      <td>57219656715;57213084303;22837185500;</td>\n",
              "      <td>Real-time data utilization barriers to improvi...</td>\n",
              "      <td>2020</td>\n",
              "      <td>Sustainability (Switzerland)</td>\n",
              "      <td>12</td>\n",
              "      <td>21</td>\n",
              "      <td>8757</td>\n",
              "      <td>1</td>\n",
              "      <td>21</td>\n",
              "      <td>NaN</td>\n",
              "      <td>10.0</td>\n",
              "      <td>10.3390/su12218757</td>\n",
              "      <td>https://www.scopus.com/inward/record.uri?eid=2...</td>\n",
              "      <td>This study presents empirical evidence for the...</td>\n",
              "      <td>Article</td>\n",
              "      <td>Final</td>\n",
              "      <td>All Open Access, Gold, Green</td>\n",
              "      <td>Scopus</td>\n",
              "      <td>2-s2.0-85094607941</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Crovini C., Ossola G., Britzelmaier B.</td>\n",
              "      <td>57200919718;6602427174;23471680600;</td>\n",
              "      <td>How to reconsider risk management in SMEs? An ...</td>\n",
              "      <td>2021</td>\n",
              "      <td>European Management Journal</td>\n",
              "      <td>39</td>\n",
              "      <td>1</td>\n",
              "      <td>NaN</td>\n",
              "      <td>118</td>\n",
              "      <td>134</td>\n",
              "      <td>NaN</td>\n",
              "      <td>9.0</td>\n",
              "      <td>10.1016/j.emj.2020.11.002</td>\n",
              "      <td>https://www.scopus.com/inward/record.uri?eid=2...</td>\n",
              "      <td>The purpose of this paper is two-fold: to reco...</td>\n",
              "      <td>Article</td>\n",
              "      <td>Final</td>\n",
              "      <td>NaN</td>\n",
              "      <td>Scopus</td>\n",
              "      <td>2-s2.0-85096819200</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-0210e736-c9f9-4165-86b1-4540d7f4e3fa')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-0210e736-c9f9-4165-86b1-4540d7f4e3fa button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-0210e736-c9f9-4165-86b1-4540d7f4e3fa');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 5
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Keeping only columns of interest\n",
        "\n",
        "data = data[['Authors', 'Author(s) ID', 'Title', 'Abstract', 'Year', 'Source title']]"
      ],
      "metadata": {
        "id": "I1seIHLzpHxq"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Combining the title and abstract in one str in a new column\n",
        "\n",
        "data['text'] = data['Title'] + '. ' + data['Abstract']"
      ],
      "metadata": {
        "id": "DvvBql308Xaf"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Creating a function for cleaning the data\n",
        "def data_prepro(text):\n",
        "  \"\"\"\n",
        "  takes in a pandas series (1 column of a dataframe), lowercasing and normalizing the text\n",
        "  \"\"\"\n",
        "  text_clean = text.map(lambda t: prepro.clean(t))\n",
        "  text_clean = text_clean.str.replace('#','')\n",
        "\n",
        "  clean_container = []\n",
        "\n",
        "  pbar = tqdm.tqdm(total=len(text_clean),position=0, leave=True)\n",
        "\n",
        "  for text in nlp.pipe(text_clean, disable=[\"tagger\", \"parser\", \"ner\"]):\n",
        "\n",
        "    txt = [token.lemma_.lower() for token in text \n",
        "          if token.is_alpha \n",
        "          and not token.is_stop \n",
        "          and not token.is_punct]\n",
        "\n",
        "    clean_container.append(\" \".join(txt))\n",
        "    pbar.update(1)\n",
        "  \n",
        "  return clean_container"
      ],
      "metadata": {
        "id": "uY_G1ml3rWiM"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "data['text_clean'] = data_prepro(data['text'])"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "j3NQJ8cRxOrw",
        "outputId": "3c566a1f-bda4-400b-ae98-4577af0979c8"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "  0%|          | 0/135 [00:00<?, ?it/s]/usr/local/lib/python3.7/dist-packages/spacy/pipeline/lemmatizer.py:211: UserWarning: [W108] The rule-based lemmatizer did not find POS annotation for one or more tokens. Check that your pipeline includes components that assign token.pos, typically 'tagger'+'attribute_ruler' or 'morphologizer'.\n",
            "  warnings.warn(Warnings.W108)\n",
            "100%|██████████| 135/135 [00:02<00:00, 52.47it/s] \n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "data.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 435
        },
        "id": "PGm9oNi6-3DK",
        "outputId": "8da7008d-bd95-495d-85b2-01412999df46"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "                                             Authors  \\\n",
              "0                    Gao Y., Hu Y., Liu X., Zhang H.   \n",
              "1  Xu X., Hu W., Liu W., Wang D., Huang Q., Huang...   \n",
              "2   Xu X., Hu W., Liu W., Wang D., Huang Q., Chen Z.   \n",
              "3           Saabye H., Kristensen T.B., Wæhrens B.V.   \n",
              "4             Crovini C., Ossola G., Britzelmaier B.   \n",
              "\n",
              "                                        Author(s) ID  \\\n",
              "0   57196280682;56580618100;35208483000;57169423400;   \n",
              "1  57205534107;24921323300;57193691954;5676303010...   \n",
              "2  57205534107;24921323300;57193691954;5676303010...   \n",
              "3               57219656715;57213084303;22837185500;   \n",
              "4                57200919718;6602427174;23471680600;   \n",
              "\n",
              "                                               Title  \\\n",
              "0  Can Public R&D Subsidy Facilitate Firms’ Explo...   \n",
              "1  Risk-based scheduling of an off-grid hybrid el...   \n",
              "2  Study on the economic benefits of retired elec...   \n",
              "3  Real-time data utilization barriers to improvi...   \n",
              "4  How to reconsider risk management in SMEs? An ...   \n",
              "\n",
              "                                            Abstract  Year  \\\n",
              "0  Public R&D subsidy is a commonly adopted polic...  2021   \n",
              "1  Making full use of renewable energy to supply ...  2021   \n",
              "2  The lithium-ion batteries of battery electric ...  2021   \n",
              "3  This study presents empirical evidence for the...  2020   \n",
              "4  The purpose of this paper is two-fold: to reco...  2021   \n",
              "\n",
              "                    Source title  \\\n",
              "0                Research Policy   \n",
              "1  Journal of Cleaner Production   \n",
              "2  Journal of Cleaner Production   \n",
              "3   Sustainability (Switzerland)   \n",
              "4    European Management Journal   \n",
              "\n",
              "                                                text  \\\n",
              "0  Can Public R&D Subsidy Facilitate Firms’ Explo...   \n",
              "1  Risk-based scheduling of an off-grid hybrid el...   \n",
              "2  Study on the economic benefits of retired elec...   \n",
              "3  Real-time data utilization barriers to improvi...   \n",
              "4  How to reconsider risk management in SMEs? An ...   \n",
              "\n",
              "                                          text_clean  \n",
              "0  public subsidy facilitate firms exploratory in...  \n",
              "1  risk based scheduling grid hybrid electricity ...  \n",
              "2  study economic benefits retired electric vehic...  \n",
              "3  real time data utilization barriers improving ...  \n",
              "4  reconsider risk management smes advanced reaso...  "
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-1fac5ea8-fc56-4635-9bc4-b9535d6f7835\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>Authors</th>\n",
              "      <th>Author(s) ID</th>\n",
              "      <th>Title</th>\n",
              "      <th>Abstract</th>\n",
              "      <th>Year</th>\n",
              "      <th>Source title</th>\n",
              "      <th>text</th>\n",
              "      <th>text_clean</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Gao Y., Hu Y., Liu X., Zhang H.</td>\n",
              "      <td>57196280682;56580618100;35208483000;57169423400;</td>\n",
              "      <td>Can Public R&amp;D Subsidy Facilitate Firms’ Explo...</td>\n",
              "      <td>Public R&amp;D subsidy is a commonly adopted polic...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Research Policy</td>\n",
              "      <td>Can Public R&amp;D Subsidy Facilitate Firms’ Explo...</td>\n",
              "      <td>public subsidy facilitate firms exploratory in...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>Xu X., Hu W., Liu W., Wang D., Huang Q., Huang...</td>\n",
              "      <td>57205534107;24921323300;57193691954;5676303010...</td>\n",
              "      <td>Risk-based scheduling of an off-grid hybrid el...</td>\n",
              "      <td>Making full use of renewable energy to supply ...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Journal of Cleaner Production</td>\n",
              "      <td>Risk-based scheduling of an off-grid hybrid el...</td>\n",
              "      <td>risk based scheduling grid hybrid electricity ...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Xu X., Hu W., Liu W., Wang D., Huang Q., Chen Z.</td>\n",
              "      <td>57205534107;24921323300;57193691954;5676303010...</td>\n",
              "      <td>Study on the economic benefits of retired elec...</td>\n",
              "      <td>The lithium-ion batteries of battery electric ...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Journal of Cleaner Production</td>\n",
              "      <td>Study on the economic benefits of retired elec...</td>\n",
              "      <td>study economic benefits retired electric vehic...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>Saabye H., Kristensen T.B., Wæhrens B.V.</td>\n",
              "      <td>57219656715;57213084303;22837185500;</td>\n",
              "      <td>Real-time data utilization barriers to improvi...</td>\n",
              "      <td>This study presents empirical evidence for the...</td>\n",
              "      <td>2020</td>\n",
              "      <td>Sustainability (Switzerland)</td>\n",
              "      <td>Real-time data utilization barriers to improvi...</td>\n",
              "      <td>real time data utilization barriers improving ...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Crovini C., Ossola G., Britzelmaier B.</td>\n",
              "      <td>57200919718;6602427174;23471680600;</td>\n",
              "      <td>How to reconsider risk management in SMEs? An ...</td>\n",
              "      <td>The purpose of this paper is two-fold: to reco...</td>\n",
              "      <td>2021</td>\n",
              "      <td>European Management Journal</td>\n",
              "      <td>How to reconsider risk management in SMEs? An ...</td>\n",
              "      <td>reconsider risk management smes advanced reaso...</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-1fac5ea8-fc56-4635-9bc4-b9535d6f7835')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-1fac5ea8-fc56-4635-9bc4-b9535d6f7835 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-1fac5ea8-fc56-4635-9bc4-b9535d6f7835');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 10
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Preprocessing the text into tokens\n",
        "tokens = []\n",
        "\n",
        "for text in nlp.pipe(data['text_clean'], disable=[\"ner\"]):\n",
        "  proj_tok = [token.lemma_.lower() for token in text \n",
        "              if token.pos_ in ['NOUN', 'PROPN', 'ADJ', 'ADV'] \n",
        "              and not token.is_stop\n",
        "              and not token.is_punct] \n",
        "  tokens.append(proj_tok)"
      ],
      "metadata": {
        "id": "sWPsPmZ4xgIa"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Adding a column 'tokens' to the dataframe, adding the tokens as values\n",
        "data['tokens'] = tokens"
      ],
      "metadata": {
        "id": "WzB9ebx6x__6"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Creating a dictionary from the abstracts\n",
        "dictionary = Dictionary(data['tokens'])"
      ],
      "metadata": {
        "id": "sKQaSCf0yYyn"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Filtering out low-frequency and high-frequency words and limiting the vocabulary of the dictionary to 100 words\n",
        "dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=1000)"
      ],
      "metadata": {
        "id": "k1WnhdqPzBlw"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Constructing a corpus (machine readable text) from the dictionary\n",
        "corpus = [dictionary.doc2bow(doc) for doc in data['tokens']]"
      ],
      "metadata": {
        "id": "6N0MY47QzNte"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Training the model\n",
        "\n",
        "lda_model = LdaMulticore(corpus, id2word=dictionary, num_topics=10, workers=4, passes=10)"
      ],
      "metadata": {
        "id": "6WEMe5FKzitb"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Visualizing the model\n",
        "\n",
        "lda_display = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "p61c4ue_03Pw",
        "outputId": "f620b56d-4f14-4233-8f2f-f3c77275afab"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "/usr/local/lib/python3.7/dist-packages/pyLDAvis/_prepare.py:247: FutureWarning: In a future version of pandas all arguments of DataFrame.drop except for the argument 'labels' will be keyword-only\n",
            "  by='saliency', ascending=False).head(R).drop('saliency', 1)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Showing the visualization\n",
        "\n",
        "pyLDAvis.display(lda_display)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 861
        },
        "id": "c-a284xX1QKs",
        "outputId": "5e6eeade-bf9a-4fb7-e08f-ea677df537ed"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<IPython.core.display.HTML object>"
            ],
            "text/html": [
              "\n",
              "<link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.3.1/pyLDAvis/js/ldavis.v1.0.0.css\">\n",
              "\n",
              "\n",
              "<div id=\"ldavis_el721396825743015204915803559\"></div>\n",
              "<script type=\"text/javascript\">\n",
              "\n",
              "var ldavis_el721396825743015204915803559_data = {\"mdsDat\": {\"x\": [0.005775303416062494, -0.016649819741709895, -0.030272266868568008, 0.07392050292970975, -0.10263145747557022, 0.014410835157799454, 0.07272611306994291, -0.15423415131872623, 0.20414999319029076, -0.06719505235923094], \"y\": [0.08922010911698429, 0.0668000048496107, -0.03176068852565361, -0.11247145885747074, -0.049334423652417025, 0.11339592373119252, 0.027551132107073925, 0.08334507902361193, -0.0016414339881150278, -0.18510424380481702], \"topics\": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], \"cluster\": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], \"Freq\": [19.083912590553645, 17.62337812705556, 10.842202398508938, 10.227923441170025, 9.940583671873435, 8.76931777339295, 6.825489904461364, 6.562774642599421, 5.295062839310435, 4.829354611074228]}, \"tinfo\": {\"Term\": [\"innovation\", \"policy\", \"firm\", \"model\", \"market\", \"risk\", \"accounting\", \"research\", \"business\", \"collaborative\", \"system\", \"sustainable\", \"company\", \"green\", \"service\", \"new\", \"danish\", \"collaboration\", \"industry\", \"platform\", \"application\", \"critical\", \"social\", \"project\", \"management\", \"literature\", \"role\", \"work\", \"capacity\", \"technology\", \"province\", \"experience\", \"supplier\", \"learning\", \"ability\", \"corporate\", \"evolution\", \"proposition\", \"competition\", \"complex\", \"stakeholder\", \"local\", \"wide\", \"customer\", \"capability\", \"power\", \"evidence\", \"price\", \"initial\", \"long\", \"opportunity\", \"critical\", \"nature\", \"adoption\", \"industry\", \"actor\", \"online\", \"instead\", \"technology\", \"government\", \"regulation\", \"resource\", \"case\", \"study\", \"time\", \"firm\", \"effect\", \"practice\", \"organizational\", \"value\", \"project\", \"process\", \"perspective\", \"sector\", \"performance\", \"finding\", \"level\", \"paper\", \"high\", \"research\", \"approach\", \"understanding\", \"review\", \"limitation\", \"effort\", \"aim\", \"scholar\", \"emerald\", \"topic\", \"demonstrate\", \"entrepreneurial\", \"medium\", \"practical\", \"pattern\", \"theoretical\", \"originality\", \"qualitative\", \"author\", \"ecosystem\", \"purpose\", \"publishing\", \"context\", \"specific\", \"influence\", \"academic\", \"systematic\", \"current\", \"strategy\", \"gap\", \"finding\", \"motivation\", \"theory\", \"practice\", \"literature\", \"research\", \"study\", \"knowledge\", \"paper\", \"approach\", \"challenge\", \"work\", \"problem\", \"market\", \"structure\", \"framework\", \"different\", \"analysis\", \"design\", \"case\", \"implication\", \"performance\", \"new\", \"firm\", \"process\", \"product\", \"department\", \"skill\", \"balance\", \"risk\", \"use\", \"organisation\", \"public\", \"patent\", \"parameter\", \"technique\", \"quality\", \"quantitative\", \"innovative\", \"economy\", \"function\", \"green\", \"transition\", \"address\", \"management\", \"technological\", \"introduction\", \"production\", \"output\", \"measure\", \"employee\", \"role\", \"assessment\", \"crucial\", \"turn\", \"user\", \"work\", \"danish\", \"innovation\", \"performance\", \"new\", \"information\", \"paper\", \"design\", \"sector\", \"model\", \"literature\", \"development\", \"study\", \"system\", \"european\", \"attention\", \"major\", \"benefit\", \"user\", \"danish\", \"sustainable\", \"christian\", \"system\", \"book\", \"denmark\", \"theoretically\", \"consumption\", \"chapter\", \"loss\", \"environmental\", \"lund\", \"introduction\", \"journal\", \"finally\", \"transition\", \"goal\", \"world\", \"general\", \"regulation\", \"capital\", \"path\", \"emergence\", \"development\", \"simple\", \"interest\", \"discussion\", \"key\", \"challenge\", \"ecosystem\", \"important\", \"economic\", \"innovation\", \"new\", \"different\", \"technology\", \"market\", \"method\", \"policy\", \"research\", \"article\", \"patent\", \"experience\", \"role\", \"study\", \"performance\", \"strategy\", \"scenario\", \"effective\", \"service\", \"network\", \"company\", \"optimization\", \"energy\", \"example\", \"china\", \"positively\", \"significantly\", \"modelling\", \"consequence\", \"accounting\", \"standard\", \"significant\", \"private\", \"logic\", \"economic\", \"multi\", \"concept\", \"relationship\", \"demand\", \"point\", \"direction\", \"failure\", \"sme\", \"gap\", \"clean\", \"switzerland\", \"industrial\", \"customer\", \"result\", \"model\", \"country\", \"international\", \"impact\", \"theory\", \"policy\", \"value\", \"sustainable\", \"high\", \"role\", \"system\", \"study\", \"effect\", \"different\", \"university\", \"collaboration\", \"difference\", \"characteristic\", \"order\", \"scale\", \"matthew\", \"component\", \"christian\", \"capital\", \"addition\", \"global\", \"relatively\", \"activity\", \"foundation\", \"survey\", \"sample\", \"path\", \"country\", \"firm\", \"multinational\", \"low\", \"insight\", \"lund\", \"chain\", \"investigate\", \"institution\", \"uk\", \"strategic\", \"model\", \"internationalisation\", \"business\", \"buyer\", \"management\", \"international\", \"non\", \"analysis\", \"capability\", \"economy\", \"datum\", \"research\", \"value\", \"high\", \"result\", \"innovation\", \"level\", \"time\", \"industry\", \"study\", \"capacity\", \"central\", \"behavior\", \"specifically\", \"driver\", \"long\", \"addition\", \"difficult\", \"unique\", \"technological\", \"environmental\", \"regional\", \"external\", \"decade\", \"local\", \"term\", \"implementation\", \"turn\", \"condition\", \"manager\", \"multi\", \"effect\", \"relevant\", \"conceptual\", \"control\", \"collaborative\", \"manufacturing\", \"innovation\", \"second\", \"hand\", \"observation\", \"industrial\", \"change\", \"positive\", \"literature\", \"enterprise\", \"framework\", \"firm\", \"process\", \"system\", \"role\", \"study\", \"level\", \"decision\", \"policy\", \"year\", \"different\", \"factor\", \"model\", \"author\", \"value\", \"paper\", \"venture\", \"platform\", \"creation\", \"mechanism\", \"supply\", \"phenomenon\", \"cost\", \"stage\", \"member\", \"contribution\", \"green\", \"accounting\", \"uncertainty\", \"dynamic\", \"light\", \"business\", \"similar\", \"strategic\", \"price\", \"society\", \"increase\", \"buyer\", \"small\", \"chain\", \"issue\", \"industry\", \"service\", \"parameter\", \"data\", \"lund\", \"new\", \"datum\", \"social\", \"high\", \"level\", \"decision\", \"value\", \"paper\", \"research\", \"model\", \"technology\", \"market\", \"development\", \"informa\", \"collaborative\", \"application\", \"science\", \"taylor\", \"francis\", \"agenda\", \"project\", \"uk\", \"methodological\", \"trading\", \"limited\", \"hand\", \"overview\", \"comprehensive\", \"particular\", \"examine\", \"overall\", \"potential\", \"collaboration\", \"complex\", \"group\", \"organization\", \"early\", \"scholar\", \"stakeholder\", \"standard\", \"critical\", \"sustainability\", \"corporate\", \"innovation\", \"social\", \"article\", \"performance\", \"impact\", \"strategy\", \"research\", \"development\", \"sustainable\", \"firm\", \"future\", \"review\", \"abstract\", \"available\", \"entrepreneur\", \"entrepreneurship\", \"regional\", \"springer\", \"licence\", \"policy\", \"reporting\", \"exclusive\", \"choice\", \"growth\", \"hand\", \"period\", \"debate\", \"point\", \"direction\", \"industrial\", \"governance\", \"nature\", \"dimension\", \"relation\", \"focus\", \"evidence\", \"market\", \"idea\", \"sample\", \"structure\", \"european\", \"recent\", \"social\", \"risk\", \"work\", \"future\", \"innovation\", \"paper\", \"important\", \"result\", \"business\", \"value\", \"development\", \"new\", \"danish\", \"different\"], \"Freq\": [124.0, 68.0, 122.0, 76.0, 59.0, 34.0, 35.0, 107.0, 65.0, 23.0, 60.0, 45.0, 34.0, 29.0, 30.0, 68.0, 40.0, 22.0, 51.0, 18.0, 22.0, 31.0, 34.0, 21.0, 40.0, 63.0, 55.0, 35.0, 22.0, 44.0, 6.3585304579880155, 21.30385095982224, 23.1654939097264, 28.073602762144528, 4.705711811169249, 6.54692254457165, 5.112395276483496, 6.750617868273249, 5.380401403328246, 4.083620070604097, 16.232789025416363, 10.105722472663343, 3.7831877357420436, 10.448205717951588, 15.752205795502302, 4.535407090238653, 11.40255268190336, 10.25725250193652, 2.904436551490669, 3.7842147535316997, 5.288584424446256, 15.631711742848234, 5.983532110519237, 6.553483605870349, 25.047022270111057, 5.8705283839217905, 4.128973811590001, 4.038756011211535, 21.55352197817415, 8.029191476924037, 5.399475463645351, 8.517863770214088, 19.852663214866137, 51.11835457089884, 11.254422625265184, 38.93060432733049, 13.33030356334346, 15.831457844067778, 10.464194448204585, 21.81876016682971, 8.939841613777798, 14.53745086457553, 10.700645590927365, 10.834660109783147, 15.254995996803178, 12.27632426562256, 11.95545482660716, 15.012357087171635, 10.245927813210132, 13.01524920780334, 9.477708120288005, 10.172913507713824, 23.16579762002058, 5.88762833804347, 9.119083076725545, 4.049414051809534, 6.0739605632164455, 7.859321854265515, 9.56778569896943, 3.85260747987844, 12.917279244923243, 6.152133662565645, 8.232131303648192, 4.0645523461828414, 8.320898359855846, 9.358649695327852, 6.976739799240499, 27.705373298804776, 15.99465642742318, 14.786106946459928, 7.338016465316809, 11.895825914019069, 10.302251520077123, 7.109981501623697, 4.050194338454644, 2.953962973195451, 9.332890644663232, 19.704804892610994, 4.790392981399624, 20.803143821690007, 2.655481045596483, 12.567398261896784, 20.5111349444738, 27.49094398402478, 42.44321982657384, 48.26914797139775, 14.305405237184884, 31.044397575787748, 19.88877199730942, 14.00116904820234, 14.226367785601187, 10.884260727541653, 18.05101922551923, 10.190041448402376, 11.760797394712469, 17.33626424622902, 13.309822668265452, 12.594043104342187, 13.333196287306409, 10.777554977276667, 13.15025602403539, 12.404488176843202, 10.746386390564815, 10.486980292867305, 10.7751619314833, 6.666870300974329, 11.028550357704, 6.391957919731415, 22.16486696865194, 8.378681100001547, 11.52672248760064, 11.372032554569042, 16.930689566367427, 4.818218727746464, 4.002312965853396, 6.4120316718172825, 4.116469414420006, 5.419839129908548, 12.760888921608071, 2.4903155217398956, 12.53863091677299, 5.313668169315508, 2.872275302641018, 17.241425917130297, 10.245204740962661, 4.369961624910206, 8.56761498250374, 3.533551354147163, 7.657243667777897, 6.735091623597872, 21.782325787578873, 3.254510858131161, 2.849921073462812, 2.347437384022414, 4.779848746130265, 11.644060496749956, 11.713825740546516, 21.492460141018157, 12.707802747102392, 12.708945415380622, 7.142740961588964, 12.956530947228458, 8.202303378585851, 7.26721335828104, 10.062836688700758, 8.998003835757132, 7.455526617793718, 7.723138001295345, 7.2163014468661375, 9.471070642689835, 3.667602115820754, 4.63677581299254, 4.903109721130143, 6.772598019786304, 20.17706146526174, 22.535868596095145, 3.166951277406825, 27.84342563551741, 5.405601093728549, 7.449858935057271, 2.36411409717301, 6.731084003411133, 9.790906433601455, 3.507579767348604, 7.677434880232041, 2.661388363994063, 4.2162977399230375, 2.2553177672426736, 2.977541285622652, 4.795133461981701, 4.354542125646634, 6.227373575703528, 2.47652207842069, 4.185710687837176, 5.55759856908325, 2.018839412637627, 2.0293799989981545, 22.325933095441734, 2.020437314580387, 3.7106573872050572, 3.315869189693564, 7.383111820421252, 10.710031418877984, 9.090232325601987, 8.325519677735048, 8.758479722537746, 24.3839705489543, 15.201006210688933, 14.47074275700106, 10.88307372123332, 12.335284334850414, 5.845153466361899, 10.973744178439398, 12.291353819225742, 5.596263211953114, 6.069257249200394, 5.883184842355268, 6.767186109271973, 8.126631311455576, 6.022319534509677, 5.601980950421243, 6.95373420177488, 4.988592864329413, 19.559676248886483, 8.999992997122064, 21.22144388207334, 5.956334505354962, 12.50501542428427, 7.275926708184816, 8.746854107981509, 5.005488860605974, 6.524343199287059, 4.046109292927877, 5.01440562621422, 18.043413020008828, 4.807025507069483, 7.07264138268301, 2.832673986767088, 8.8539832277468, 13.660764963002302, 3.0066764617944757, 8.473368864852675, 14.77246117970248, 2.4393997197842516, 4.937531580019574, 3.035885162356808, 5.5986556968127505, 4.672992380575861, 3.5800554551533597, 2.059888376612393, 2.6263423091904423, 3.877047811613099, 6.268402525485561, 11.628291050023755, 20.812244568950305, 7.745603071492673, 8.539562141307362, 9.958797186941576, 7.589726590210559, 11.259573133539831, 11.37215115800352, 8.492215035641081, 6.932638710906564, 7.236787647722426, 7.0975411141052716, 7.596051291295476, 6.078675495496574, 6.193827444805528, 12.891594156435538, 15.053815759445246, 9.477604374232271, 8.193686089954872, 5.629471103645496, 4.788835609179322, 2.4076666192661014, 3.8499836464456583, 2.7193756416441888, 6.026101176308218, 2.9017486975254374, 8.40695461130331, 2.9033441589130926, 9.467823294741526, 3.3922448478761837, 3.674371158165345, 3.1765380752253023, 1.8780169537001683, 7.962622966354959, 37.86288886221425, 1.76452905918359, 4.25806999094474, 5.157422844064448, 1.8711947630524983, 4.7415467288239865, 2.9098107887922486, 2.3773073725654825, 3.687320981749431, 1.8195933923970098, 21.128194030799023, 4.125052924726816, 15.852214621159856, 3.0445760404863167, 9.899987546316488, 6.720540414096839, 6.635391681393519, 8.721075495159726, 6.60250996054754, 6.474125712175662, 7.066881588739527, 14.62697326857139, 10.030808080791141, 6.23392665606175, 6.57452270984627, 10.331108557610522, 6.22645103652445, 4.931326622254153, 5.474438186289107, 4.797849699313903, 11.799423028666592, 3.695953788366495, 2.793698722648952, 2.7944702909562884, 2.784081105124419, 2.7210467495261565, 2.70736610704931, 1.863920235561956, 2.749329721005012, 7.80712189350121, 5.924329590980474, 3.705177646024185, 1.7188668141151089, 1.7354567345426448, 5.308529365573639, 2.8430120109227723, 4.954159907252869, 1.8918096656866588, 5.3369399484632805, 4.598183506612033, 1.8917460784939555, 10.190639083651153, 3.427011429059243, 4.598787912711748, 2.7966178336706773, 6.225522238160806, 1.6954036862893496, 32.20560639829034, 1.8905770356040512, 1.85298629759466, 1.9026476765831755, 2.7976050740027496, 5.987566726354779, 2.795910945119492, 12.01306812969254, 3.9721988417635794, 6.09943298677145, 17.80290359718697, 8.440264160013534, 7.758264204185418, 6.987708047627255, 11.874624607852827, 5.809245949720635, 4.333557646977149, 6.183980790721607, 3.665571783990364, 5.233016624317269, 3.5694723066991236, 4.6493312089159, 4.166850382775273, 4.15984879917185, 4.070335949886289, 11.000941721055106, 13.737524508885583, 9.351466528470501, 4.486220779353184, 4.6336405756700225, 4.306348617725756, 5.399097873681972, 4.46476347542699, 3.4044699464144403, 6.036765211522161, 11.515819527924569, 12.100775618719682, 3.7437604132163873, 3.4522692172288, 2.268428739293016, 19.188796608728687, 1.9232104527651006, 1.9090216298561264, 5.582505632897428, 1.5749798278476956, 2.83720970223518, 3.059704850045627, 7.259311322596706, 4.351096996421282, 4.764927054445298, 11.807281519724805, 7.109491740467505, 1.9172994412045143, 1.6125173985434667, 1.398241548655672, 14.019628554609593, 6.5983760212145866, 6.733471650469475, 5.917700370000006, 7.1690565169469425, 4.837258893144491, 9.970861709724314, 10.72777541727278, 11.1329194356317, 9.064560389896956, 6.516678252560613, 4.94857306940504, 4.871593772977825, 5.675664036536183, 13.469088356148154, 11.940913210695019, 8.218758070554273, 6.084380348418008, 6.077175864392319, 3.8689479430609635, 9.06735271524673, 5.521084966315543, 2.3189449061827023, 5.218495281098439, 4.8280637801565405, 2.5403197143577496, 2.913286189883208, 2.015123677990383, 3.796893609836887, 1.5457098424680351, 3.1133141966487745, 5.684176176791852, 5.848569618945463, 1.6725845355403837, 4.867498582954094, 3.271501272469479, 1.8153016347093152, 1.9962687804674344, 5.852474618804657, 2.1508956545585503, 6.970500014330763, 4.6199789565257285, 2.016295720403409, 24.57004484422161, 6.994927453109628, 4.570116807342571, 7.921306114792475, 5.0299052826893265, 5.433727630951819, 8.948389562738216, 6.6435710393158125, 5.54221800644605, 6.7280482762419735, 3.4834097276693137, 3.5482856825274647, 5.954038367579805, 5.929599792031968, 8.591904210824474, 7.187112525656505, 7.006775912414712, 4.57270906311942, 2.7793992527143825, 32.4363280610819, 4.208032108162096, 2.7796568296234514, 4.592156892794062, 5.792685760046744, 2.247551173179642, 4.780802757777149, 1.873904790369545, 3.341448765965407, 1.8822746484423851, 2.7602829025673774, 3.172530261900417, 2.7810387158258867, 2.3701528344407827, 3.4456681558095905, 1.8842228637071972, 4.542903425854046, 12.612558548726282, 1.8809983594961888, 1.8822608883313965, 4.302613545210641, 2.7797721671829745, 2.77705756011849, 6.3598138365085095, 5.471425820458399, 5.465023194432972, 3.4345175184531294, 6.637777354959013, 5.5147253337560125, 3.378859879407801, 3.6950022945722694, 4.082580403238426, 3.7037846467587925, 3.4634814698283645, 3.3955037386005267, 3.2250771882143736, 3.221224047921568], \"Total\": [124.0, 68.0, 122.0, 76.0, 59.0, 34.0, 35.0, 107.0, 65.0, 23.0, 60.0, 45.0, 34.0, 29.0, 30.0, 68.0, 40.0, 22.0, 51.0, 18.0, 22.0, 31.0, 34.0, 21.0, 40.0, 63.0, 55.0, 35.0, 22.0, 44.0, 8.308687228108186, 27.964426915305253, 30.641732008958215, 38.302774644703824, 6.4785200538468946, 9.330081836694152, 7.401508112734382, 10.321410791847342, 8.420970609294212, 6.546623045203296, 26.219594604954896, 17.417138169224344, 6.593048215766169, 18.822358110747455, 28.752603678705285, 8.395221251993185, 21.190129230019863, 19.41459158852315, 5.573786850228695, 7.3456770006021195, 10.283831407949327, 31.310046313226046, 12.016507320845374, 13.305289208216848, 51.038014617712264, 12.115805141995935, 8.570548398467832, 8.384037625939108, 44.92262837491076, 16.749376970318718, 11.326063098682177, 18.728280584969287, 49.195841520583265, 146.3912761361959, 26.29823253682002, 122.48409884820548, 36.244063893738335, 45.93433444869267, 26.370333844891206, 75.23267978911886, 21.58052937898505, 47.10872539514256, 29.247230237030145, 31.0651254871641, 61.971178685312225, 44.13468498974399, 42.88723190755875, 88.55675463457924, 31.838385902319427, 107.52857520906586, 50.73658551146674, 12.765843623497451, 30.52604568036492, 7.812531911798214, 12.641614289342781, 5.815610120526111, 8.821406297049396, 11.665717029713194, 14.56522420442659, 5.869409753564566, 20.362913340071156, 9.741130511660904, 13.507872321910494, 6.754139825849141, 14.47503628072767, 16.388712507086346, 12.512754508962448, 50.40348834009018, 29.239850426570897, 27.039482369173044, 13.493679733581516, 22.103131902474907, 19.36245536429513, 13.443713144368987, 7.700887519700164, 5.801731498435622, 18.3434080861677, 39.909279566272886, 9.800720672361754, 44.13468498974399, 5.761119133835172, 27.26651200990494, 45.93433444869267, 63.91176496479944, 107.52857520906586, 146.3912761361959, 32.51783371245965, 88.55675463457924, 50.73658551146674, 33.86156739475474, 35.54151663061185, 24.116708288182938, 59.736548705907964, 22.14335133744668, 29.40203800986767, 65.9803565209225, 40.221924280563755, 41.0779986511959, 49.195841520583265, 27.553618834707777, 61.971178685312225, 68.30276427388648, 122.48409884820548, 47.10872539514256, 15.124710009856107, 9.520400005239646, 16.275406135190742, 9.473310824621056, 34.22157543055198, 13.257560733965898, 18.283967988477915, 19.028106072831452, 28.448680729630137, 8.480948498405956, 7.724105979468488, 12.389942861121307, 8.513223109978712, 11.461100217026416, 28.599164644157774, 5.759097198737367, 29.16487942114793, 12.386614682162227, 6.751616041890907, 40.69886298954831, 24.3163414296586, 10.492752223428973, 20.84733720617688, 8.630579163502738, 19.24606717007918, 16.988139843611286, 55.13559519886401, 8.6728637451426, 7.626902080936501, 6.550568866001909, 13.37194536774028, 35.54151663061185, 40.87147459548926, 124.82895638714348, 61.971178685312225, 68.30276427388648, 27.170489398207675, 88.55675463457924, 41.0779986511959, 31.0651254871641, 76.85988044201615, 63.91176496479944, 62.93683907259506, 146.3912761361959, 60.733571825602844, 15.140267122429215, 6.612559177235847, 8.594028935612991, 9.554347471934083, 13.37194536774028, 40.87147459548926, 45.99871128608502, 6.652851114741574, 60.733571825602844, 12.266861245012013, 17.191197668713144, 5.668886430109668, 16.229408058082488, 23.701411690171632, 8.543289771370382, 18.70404629221933, 6.6082020245833695, 10.492752223428973, 5.785656108849824, 7.662570727039294, 12.386614682162227, 11.357437274314265, 16.387389403238874, 6.563755340058511, 11.326063098682177, 15.123051480452471, 5.668097573627837, 5.718266112598694, 62.93683907259506, 5.707512409103602, 10.570976943587675, 9.497461709559394, 21.88988572075582, 33.86156739475474, 29.239850426570897, 27.573362350161123, 30.08792782643074, 124.82895638714348, 68.30276427388648, 65.9803565209225, 44.92262837491076, 59.736548705907964, 19.432100728758478, 68.57642242140511, 107.52857520906586, 22.108088559970998, 28.448680729630137, 27.964426915305253, 55.13559519886401, 146.3912761361959, 61.971178685312225, 39.909279566272886, 8.777957529165798, 7.8360612328361245, 30.775320974718596, 14.47045217064655, 34.57640416908017, 9.720152323127621, 21.335718338190453, 12.536634288683542, 15.266022930718576, 8.795429235404379, 11.602372878568563, 7.705192518848546, 9.566595698838649, 35.2938416786623, 9.661338274196636, 14.337042459695589, 5.844138825446906, 18.399304301902916, 30.08792782643074, 6.682918777904149, 19.170911002983004, 34.660208285188155, 5.72800527091353, 12.295709441856738, 7.583696971570697, 14.160642504960503, 12.667677601739475, 9.800720672361754, 5.775895784366761, 7.5334462800753, 11.265192947714162, 18.822358110747455, 38.21351174508077, 76.85988044201615, 24.690185463762006, 28.033108917588663, 34.46805464975846, 27.26651200990494, 68.57642242140511, 75.23267978911886, 45.99871128608502, 31.838385902319427, 55.13559519886401, 60.733571825602844, 146.3912761361959, 36.244063893738335, 65.9803565209225, 18.071067654062112, 22.630086539127536, 15.090077864700358, 14.24292908668394, 10.370310065942164, 9.467876324813743, 5.599863968888647, 9.415457970948262, 6.652851114741574, 15.123051480452471, 7.456523014163269, 21.64221934769166, 7.553800876866813, 25.29496488357551, 9.360999018031915, 10.546440680047775, 9.44787503382831, 5.668097573627837, 24.690185463762006, 122.48409884820548, 5.737097997435528, 14.029091759576458, 17.8166328569844, 6.6082020245833695, 16.757614200744825, 10.288515408081773, 8.54726295632787, 13.296946099375315, 6.572290764348888, 76.85988044201615, 15.046643742402377, 65.58865169996491, 11.129345148753712, 40.69886298954831, 28.033108917588663, 27.73797393494528, 40.221924280563755, 28.752603678705285, 28.599164644157774, 32.797766257887076, 107.52857520906586, 75.23267978911886, 31.838385902319427, 38.21351174508077, 124.82895638714348, 42.88723190755875, 26.29823253682002, 51.038014617712264, 146.3912761361959, 22.179966892286004, 8.24706191553933, 6.529943545751305, 7.431109373349882, 7.493642075906231, 7.3456770006021195, 7.456523014163269, 5.573007745261787, 8.344320156986019, 24.3163414296586, 18.70404629221933, 11.764212017008497, 5.572866537479289, 5.672462095484671, 17.417138169224344, 9.366056891803078, 16.847865878993435, 6.550568866001909, 18.528957637207302, 16.17959598231088, 6.682918777904149, 36.244063893738335, 12.24378151556512, 16.707709627613333, 10.307582413180226, 23.540340504003947, 6.488058519095908, 124.82895638714348, 7.466104693782128, 7.398569583432864, 7.599591630135562, 11.265192947714162, 25.175856394055334, 11.298335360112851, 63.91176496479944, 17.166837078114614, 29.40203800986767, 122.48409884820548, 47.10872539514256, 60.733571825602844, 55.13559519886401, 146.3912761361959, 42.88723190755875, 25.130810029538786, 68.57642242140511, 18.86824731589342, 65.9803565209225, 18.047926432755435, 76.85988044201615, 50.40348834009018, 75.23267978911886, 88.55675463457924, 14.744314301679674, 18.594709730779968, 19.316835893500002, 9.411146675366842, 10.357019825744732, 10.334637230716734, 13.164019966618001, 11.08461500488852, 8.459494313199867, 15.05493918080673, 29.16487942114793, 35.2938416786623, 11.39528367411761, 11.103610376874789, 7.637410116781643, 65.58865169996491, 6.588731768655183, 6.572290764348888, 19.41459158852315, 5.61431670988284, 10.273496125910315, 11.129345148753712, 26.704908330482343, 16.757614200744825, 18.972635602334208, 51.038014617712264, 30.775320974718596, 8.480948498405956, 7.490689175635477, 6.6082020245833695, 68.30276427388648, 32.797766257887076, 34.8889083173415, 31.838385902319427, 42.88723190755875, 25.130810029538786, 75.23267978911886, 88.55675463457924, 107.52857520906586, 76.85988044201615, 44.92262837491076, 59.736548705907964, 62.93683907259506, 9.546362538012481, 23.540340504003947, 22.120231559621892, 15.29312373679382, 11.51040753699033, 11.51035369704244, 7.629831592117138, 21.58052937898505, 13.296946099375315, 5.6632072485048175, 13.205081268262534, 13.41239081573221, 7.398569583432864, 9.582357431910982, 6.753774938229634, 13.371204174856562, 5.61112221292954, 11.40106723063295, 21.02427037751647, 22.630086539127536, 6.546623045203296, 19.138465384076643, 13.330239744684809, 7.567544020024726, 8.821406297049396, 26.219594604954896, 9.661338274196636, 31.310046313226046, 20.770643743264326, 9.330081836694152, 124.82895638714348, 34.8889083173415, 22.108088559970998, 61.971178685312225, 34.46805464975846, 39.909279566272886, 107.52857520906586, 62.93683907259506, 45.99871128608502, 122.48409884820548, 22.959724722109566, 30.52604568036492, 8.1564352310317, 9.222543260635161, 13.794288169097108, 11.813458570762343, 11.764212017008497, 8.303916853526763, 5.51081598778876, 68.57642242140511, 9.245731188555581, 6.452396351045882, 11.3357483364247, 18.03290430331197, 7.398569583432864, 16.562050253763033, 6.605318415583854, 12.295709441856738, 7.583696971570697, 11.265192947714162, 12.961060007189634, 12.016507320845374, 10.277446714921272, 15.043783061917004, 8.433274717417737, 21.190129230019863, 59.736548705907964, 9.378159963748564, 9.44787503382831, 22.14335133744668, 15.140267122429215, 15.17470975409201, 34.8889083173415, 34.22157543055198, 35.54151663061185, 22.959724722109566, 124.82895638714348, 88.55675463457924, 27.573362350161123, 38.21351174508077, 65.58865169996491, 75.23267978911886, 62.93683907259506, 68.30276427388648, 40.87147459548926, 65.9803565209225], \"Category\": [\"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Default\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic1\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic2\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic3\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic4\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic5\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic6\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic7\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic8\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic9\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\", \"Topic10\"], \"logprob\": [30.0, 29.0, 28.0, 27.0, 26.0, 25.0, 24.0, 23.0, 22.0, 21.0, 20.0, 19.0, 18.0, 17.0, 16.0, 15.0, 14.0, 13.0, 12.0, 11.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, -5.3295, -4.1204, -4.0367, -3.8445, -5.6305, -5.3003, -5.5477, -5.2697, -5.4966, -5.7723, -4.3923, -4.8662, -5.8488, -4.8329, -4.4223, -5.6674, -4.7455, -4.8513, -6.1131, -5.8485, -5.5138, -4.43, -5.3903, -5.2993, -3.9586, -5.4094, -5.7613, -5.7834, -4.1088, -5.0962, -5.493, -5.0372, -4.191, -3.2452, -4.7586, -3.5175, -4.5893, -4.4173, -4.8314, -4.0966, -4.9888, -4.5026, -4.809, -4.7966, -4.4544, -4.6716, -4.6981, -4.4704, -4.8524, -4.6132, -4.9304, -4.78, -3.957, -5.3268, -4.8893, -5.7011, -5.2957, -5.038, -4.8413, -5.751, -4.5411, -5.2829, -4.9917, -5.6974, -4.9809, -4.8634, -5.1571, -3.7781, -4.3274, -4.406, -5.1066, -4.6235, -4.7673, -5.1382, -5.7009, -6.0166, -4.8662, -4.1188, -5.5331, -4.0646, -6.1231, -4.5686, -4.0787, -3.7858, -3.3515, -3.2229, -4.4391, -3.6643, -4.1095, -4.4606, -4.4446, -4.7124, -4.2065, -4.7783, -4.6349, -4.2469, -4.5112, -4.5665, -4.5094, -4.7222, -4.5233, -4.5816, -4.7251, -4.7496, -4.2367, -4.7168, -4.2134, -4.7589, -3.5154, -4.4882, -4.1693, -4.1828, -3.7848, -5.0415, -5.2271, -4.7557, -5.1989, -4.9239, -4.0675, -5.7015, -4.0851, -4.9436, -5.5588, -3.7666, -4.2871, -5.1392, -4.4659, -5.3516, -4.5783, -4.7066, -3.5328, -5.4339, -5.5666, -5.7606, -5.0495, -4.1591, -4.1532, -3.5462, -4.0717, -4.0716, -4.6478, -4.0523, -4.5095, -4.6305, -4.3051, -4.4169, -4.605, -4.5697, -4.6376, -4.3074, -5.2561, -5.0216, -4.9657, -4.6427, -3.5511, -3.4405, -5.4028, -3.229, -4.8682, -4.5474, -5.6952, -4.6489, -4.2741, -5.3007, -4.5173, -5.5768, -5.1166, -5.7423, -5.4645, -4.988, -5.0844, -4.7266, -5.6487, -5.1239, -4.8404, -5.8531, -5.8479, -3.4498, -5.8523, -5.2444, -5.3569, -4.5564, -4.1844, -4.3484, -4.4363, -4.3856, -3.3617, -3.8342, -3.8835, -4.1684, -4.0431, -4.79, -4.1601, -4.0467, -4.8335, -4.7524, -4.7835, -4.6435, -4.4605, -4.7601, -4.8325, -4.5878, -4.9199, -3.5536, -4.3299, -3.4721, -4.7426, -4.001, -4.5425, -4.3584, -4.9166, -4.6516, -5.1293, -4.9148, -3.6343, -4.957, -4.5709, -5.4859, -4.3462, -3.9126, -5.4263, -4.3902, -3.8343, -5.6354, -4.9302, -5.4166, -4.8046, -4.9853, -5.2517, -5.8045, -5.5615, -5.172, -4.6916, -4.0737, -3.4916, -4.48, -4.3824, -4.2286, -4.5003, -4.1059, -4.0959, -4.388, -4.5909, -4.5479, -4.5674, -4.4995, -4.7223, -4.7035, -3.8452, -3.6901, -4.1528, -4.2984, -4.6737, -4.8354, -5.5231, -5.0537, -5.4013, -4.6056, -5.3364, -4.2727, -5.3359, -4.1538, -5.1802, -5.1004, -5.2459, -5.7715, -4.327, -2.7678, -5.8339, -4.9529, -4.7613, -5.7752, -4.8454, -5.3336, -5.5358, -5.0968, -5.8031, -3.3511, -4.9847, -3.6384, -5.2884, -4.1092, -4.4966, -4.5093, -4.236, -4.5143, -4.5339, -4.4463, -3.7189, -4.0961, -4.5717, -4.5185, -4.0666, -4.5729, -4.8061, -4.7016, -4.8336, -3.6831, -4.8439, -5.1238, -5.1235, -5.1272, -5.1501, -5.1552, -5.5285, -5.1398, -4.0961, -4.3721, -4.8414, -5.6095, -5.5999, -4.4818, -5.1063, -4.5509, -5.5136, -4.4765, -4.6255, -5.5136, -3.8297, -4.9195, -4.6253, -5.1227, -4.3225, -5.6232, -2.679, -5.5143, -5.5343, -5.5079, -5.1224, -4.3615, -5.123, -3.6651, -4.7718, -4.3429, -3.2718, -4.0181, -4.1024, -4.207, -3.6767, -4.3917, -4.6848, -4.3292, -4.8522, -4.4962, -4.8787, -4.6144, -4.724, -4.7257, -4.7474, -3.7139, -3.4918, -3.8764, -4.6109, -4.5785, -4.6518, -4.4257, -4.6157, -4.8868, -4.314, -3.6682, -3.6186, -4.7918, -4.8729, -5.2928, -3.1576, -5.4579, -5.4653, -4.3923, -5.6576, -5.0691, -4.9936, -4.1296, -4.6415, -4.5506, -3.6432, -4.1505, -5.461, -5.6341, -5.7767, -3.4714, -4.2251, -4.2048, -4.3339, -4.1421, -4.5355, -3.8122, -3.7391, -3.702, -3.9075, -4.2375, -4.5128, -4.5285, -4.1611, -3.2969, -3.4173, -3.7908, -4.0915, -4.0927, -4.5443, -3.6926, -4.1887, -5.0561, -4.245, -4.3228, -4.965, -4.828, -5.1966, -4.5631, -5.4618, -4.7616, -4.1596, -4.1311, -5.3829, -4.3147, -4.712, -5.301, -5.206, -4.1304, -5.1314, -3.9556, -4.3669, -5.196, -2.6957, -3.9521, -4.3777, -3.8277, -4.2819, -4.2046, -3.7058, -4.0036, -4.1849, -3.991, -4.6492, -4.6308, -4.0211, -4.0252, -3.6544, -3.8329, -3.8583, -4.2851, -4.783, -2.3259, -4.3682, -4.7829, -4.2808, -4.0486, -4.9953, -4.2406, -5.1772, -4.5988, -5.1727, -4.7899, -4.6507, -4.7824, -4.9422, -4.5681, -5.1717, -4.2916, -3.2705, -5.1734, -5.1727, -4.346, -4.7828, -4.7838, -3.9552, -4.1057, -4.1068, -4.5713, -3.9124, -4.0978, -4.5877, -4.4982, -4.3985, -4.4958, -4.5629, -4.5827, -4.6342, -4.6354], \"loglift\": [30.0, 29.0, 28.0, 27.0, 26.0, 25.0, 24.0, 23.0, 22.0, 21.0, 20.0, 19.0, 18.0, 17.0, 16.0, 15.0, 14.0, 13.0, 12.0, 11.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 1.3888, 1.3843, 1.3766, 1.3456, 1.3366, 1.3021, 1.2863, 1.2317, 1.2084, 1.1844, 1.1769, 1.112, 1.1009, 1.0677, 1.0546, 1.0406, 1.0366, 1.0183, 1.0045, 0.9931, 0.9913, 0.9617, 0.9591, 0.9482, 0.9445, 0.9318, 0.926, 0.9259, 0.9219, 0.921, 0.9155, 0.8685, 0.7489, 0.6042, 0.8076, 0.5101, 0.6561, 0.5911, 0.732, 0.4185, 0.7751, 0.4806, 0.6508, 0.603, 0.2546, 0.3768, 0.3789, -0.1184, 0.5225, -0.4553, -0.0214, 1.5089, 1.46, 1.4531, 1.4093, 1.374, 1.3628, 1.341, 1.3157, 1.3149, 1.2808, 1.2764, 1.2407, 1.2281, 1.1823, 1.1757, 1.1518, 1.1375, 1.1327, 1.1323, 1.1268, 1.1164, 1.105, 1.0989, 1.0934, 1.0609, 1.0602, 1.0302, 1.0201, 0.9838, 0.9614, 0.9614, 0.9297, 0.8923, 0.8064, 0.6265, 0.9148, 0.6877, 0.7995, 0.8528, 0.8203, 0.9404, 0.5392, 0.9598, 0.8197, 0.3994, 0.63, 0.5537, 0.4304, 0.7973, 0.1857, 0.0301, -0.6975, 0.2336, 1.8826, 1.8654, 1.8326, 1.8283, 1.7874, 1.7628, 1.7604, 1.707, 1.7028, 1.6563, 1.5643, 1.563, 1.4951, 1.4728, 1.4147, 1.3834, 1.3776, 1.3754, 1.367, 1.3628, 1.3574, 1.3458, 1.3325, 1.3287, 1.3001, 1.2965, 1.293, 1.2416, 1.2373, 1.1955, 1.193, 1.1058, 0.9721, 0.4625, 0.6373, 0.5401, 0.8857, 0.2997, 0.6107, 0.769, 0.1886, 0.2612, 0.0885, -0.7203, 0.0916, 1.8109, 1.6906, 1.663, 1.6129, 1.5998, 1.5742, 1.5665, 1.5378, 1.5001, 1.4606, 1.4438, 1.4055, 1.4, 1.396, 1.3898, 1.3896, 1.3706, 1.3683, 1.338, 1.3348, 1.331, 1.3214, 1.3125, 1.3053, 1.2846, 1.279, 1.2477, 1.2441, 1.2437, 1.2416, 1.2331, 1.2277, 1.1932, 1.1289, 1.1117, 1.0825, 1.0459, 0.647, 0.7775, 0.7628, 0.8623, 0.7026, 1.0787, 0.4476, 0.1112, 0.9062, 0.7352, 0.7212, 0.1823, -0.6111, -0.0511, 0.3166, 2.0756, 1.857, 1.8553, 1.8337, 1.8204, 1.8188, 1.7743, 1.7645, 1.7516, 1.7448, 1.7329, 1.6644, 1.6626, 1.6376, 1.6105, 1.6019, 1.5843, 1.5771, 1.5189, 1.5098, 1.4921, 1.4557, 1.4549, 1.3962, 1.393, 1.3806, 1.3113, 1.3015, 1.2775, 1.2548, 1.2419, 1.209, 1.1188, 1.0021, 1.1493, 1.1199, 1.067, 1.0297, 0.5018, 0.4191, 0.6191, 0.7841, 0.2779, 0.1618, -0.6501, 0.5231, -0.0573, 2.0962, 2.0263, 1.9688, 1.881, 1.823, 1.7523, 1.5898, 1.5396, 1.5393, 1.5138, 1.4901, 1.4883, 1.4777, 1.4512, 1.4189, 1.3795, 1.3439, 1.3293, 1.3023, 1.2599, 1.2548, 1.2416, 1.1942, 1.1722, 1.1714, 1.171, 1.1543, 1.1513, 1.1497, 1.1425, 1.1398, 1.0138, 1.1377, 1.0202, 1.0057, 1.0035, 0.9052, 0.9626, 0.9483, 0.899, 0.439, 0.419, 0.8032, 0.6739, -0.0579, 0.5041, 0.76, 0.2014, -0.9842, 2.0534, 1.8819, 1.8355, 1.7065, 1.6944, 1.6914, 1.6714, 1.5893, 1.5743, 1.5484, 1.5348, 1.5292, 1.5083, 1.5002, 1.4964, 1.4923, 1.4605, 1.4425, 1.4398, 1.4264, 1.4225, 1.4157, 1.4112, 1.3944, 1.38, 1.3544, 1.3425, 1.3297, 1.311, 1.3, 1.2997, 1.2916, 1.2483, 1.288, 1.013, 1.2208, 1.1116, 0.7559, 0.9651, 0.6268, 0.6189, 0.1726, 0.6854, 0.9268, 0.2785, 1.046, 0.1501, 1.0639, -0.1208, 0.1916, -0.2106, -0.3954, 2.4309, 2.421, 1.9983, 1.9829, 1.9194, 1.8483, 1.8325, 1.8144, 1.8136, 1.8099, 1.7945, 1.6533, 1.6106, 1.5555, 1.5098, 1.4947, 1.4924, 1.4875, 1.4774, 1.4527, 1.437, 1.4325, 1.4212, 1.3753, 1.342, 1.2599, 1.2585, 1.2369, 1.1879, 1.1707, 1.1403, 1.1202, 1.0787, 1.041, 0.935, 1.076, 0.7028, 0.6129, 0.4559, 0.5861, 0.7932, 0.2329, 0.165, 2.4184, 2.3801, 2.3219, 2.3174, 2.3009, 2.2997, 2.2593, 2.0713, 2.0594, 2.0455, 2.01, 1.9167, 1.8694, 1.7478, 1.729, 1.6795, 1.6491, 1.6404, 1.6304, 1.5853, 1.5738, 1.5693, 1.5336, 1.5108, 1.4525, 1.4388, 1.4361, 1.4361, 1.4352, 1.4064, 1.313, 1.3314, 1.362, 0.8813, 1.0138, 0.9444, 0.4521, 0.6899, 0.8222, 0.0367, 1.0527, 0.7863, 2.7157, 2.5888, 2.557, 2.5335, 2.5123, 2.4338, 2.346, 2.2818, 2.2433, 2.1883, 2.1268, 1.8949, 1.839, 1.788, 1.7706, 1.7276, 1.6369, 1.6241, 1.623, 1.567, 1.5635, 1.5566, 1.5318, 1.4905, 1.4752, 1.4239, 1.4171, 1.3921, 1.3355, 1.3322, 1.3283, 1.1971, 1.1581, 1.1306, 0.0963, 0.2542, 0.9311, 0.6942, 0.2538, 0.0192, 0.1306, 0.029, 0.491, 0.0109]}, \"token.table\": {\"Topic\": [1, 8, 8, 10, 1, 2, 6, 2, 4, 5, 7, 8, 1, 3, 6, 8, 1, 2, 7, 10, 5, 6, 7, 2, 3, 4, 5, 1, 2, 4, 1, 4, 9, 2, 7, 1, 2, 3, 5, 6, 7, 8, 9, 10, 2, 3, 4, 5, 7, 9, 1, 2, 3, 4, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 9, 2, 3, 7, 1, 4, 7, 1, 2, 3, 4, 5, 7, 8, 2, 5, 10, 1, 3, 5, 7, 8, 2, 4, 7, 3, 4, 6, 7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 6, 8, 1, 3, 4, 6, 7, 1, 4, 6, 7, 9, 4, 5, 6, 10, 1, 2, 3, 4, 6, 7, 8, 1, 7, 1, 4, 6, 8, 1, 2, 3, 4, 6, 8, 10, 1, 3, 4, 7, 9, 10, 3, 4, 6, 9, 10, 2, 3, 4, 6, 1, 5, 7, 2, 6, 10, 4, 6, 1, 2, 3, 5, 6, 7, 9, 3, 6, 7, 9, 1, 3, 5, 8, 1, 4, 1, 9, 1, 2, 6, 10, 1, 2, 5, 9, 1, 3, 4, 5, 8, 1, 3, 6, 7, 1, 2, 4, 5, 6, 7, 10, 1, 4, 5, 7, 1, 3, 4, 5, 8, 9, 1, 2, 3, 8, 10, 1, 2, 6, 8, 3, 5, 7, 10, 1, 9, 3, 4, 8, 1, 4, 5, 6, 8, 1, 2, 8, 10, 1, 2, 9, 1, 3, 4, 9, 1, 2, 3, 5, 7, 1, 5, 10, 1, 3, 4, 8, 9, 10, 1, 2, 7, 8, 1, 2, 3, 6, 7, 8, 1, 2, 3, 10, 2, 3, 7, 9, 1, 2, 3, 5, 6, 7, 8, 10, 3, 5, 10, 2, 4, 1, 3, 4, 5, 7, 1, 3, 4, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 3, 7, 2, 5, 6, 7, 8, 10, 1, 5, 9, 10, 1, 3, 4, 5, 2, 7, 9, 10, 1, 3, 7, 8, 10, 1, 2, 8, 9, 2, 3, 4, 5, 7, 3, 4, 5, 6, 8, 2, 4, 7, 9, 1, 3, 5, 7, 9, 10, 2, 5, 1, 2, 6, 10, 2, 3, 6, 7, 1, 2, 4, 6, 1, 2, 3, 7, 8, 1, 2, 4, 5, 9, 1, 2, 5, 6, 7, 8, 1, 2, 5, 6, 10, 1, 2, 5, 6, 7, 1, 8, 10, 1, 4, 5, 7, 8, 4, 5, 7, 10, 1, 6, 8, 10, 1, 8, 1, 8, 9, 1, 3, 5, 3, 7, 10, 1, 4, 1, 6, 7, 9, 1, 2, 3, 5, 6, 7, 9, 1, 5, 8, 10, 4, 5, 6, 1, 2, 3, 5, 6, 7, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 3, 4, 6, 10, 1, 6, 9, 1, 2, 6, 7, 1, 2, 4, 5, 9, 3, 4, 5, 1, 2, 4, 6, 9, 10, 2, 5, 1, 4, 6, 7, 1, 3, 4, 6, 1, 4, 5, 7, 8, 10, 1, 3, 8, 9, 10, 1, 3, 6, 7, 9, 3, 4, 8, 1, 2, 4, 5, 8, 9, 2, 4, 5, 10, 7, 9, 10, 1, 5, 6, 8, 10, 1, 2, 3, 6, 10, 1, 2, 3, 4, 5, 6, 8, 9, 10, 1, 2, 4, 5, 7, 9, 1, 2, 3, 4, 7, 8, 10, 1, 2, 3, 4, 6, 10, 1, 3, 8, 2, 5, 7, 10, 1, 4, 5, 6, 7, 8, 9, 1, 2, 5, 7, 1, 4, 9, 1, 2, 3, 4, 5, 6, 1, 3, 7, 1, 2, 3, 4, 6, 7, 9, 10, 2, 3, 4, 10, 1, 2, 4, 6, 7, 9, 1, 2, 7, 10, 1, 2, 6, 2, 3, 4, 9, 1, 2, 4, 5, 6, 1, 2, 6, 7, 1, 3, 4, 1, 5, 6, 8, 2, 3, 6, 7, 8, 9, 4, 5, 9, 1, 2, 3, 4, 6, 7, 9, 10, 1, 2, 3, 4, 6, 7, 1, 2, 3, 4, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 3, 8, 10, 2, 6, 8, 1, 2, 1, 2, 4, 5, 8, 9, 1, 2, 3, 6, 7, 8, 9, 10, 1, 7, 10, 1, 2, 3, 5, 1, 7, 1, 4, 5, 6, 1, 4, 5, 6, 8, 4, 6, 8, 2, 4, 6, 10, 1, 2, 3, 6, 7, 9, 2, 3, 4, 5, 6, 7, 1, 7, 9, 1, 2, 3, 4, 5, 7, 8, 10, 1, 6, 2, 3, 4, 7, 10, 5, 6, 8, 2, 5, 6, 8, 1, 2, 3, 8, 2, 3, 4, 5, 6, 1, 6, 9, 1, 2, 3, 5, 6, 7, 8, 5, 6, 9, 1, 2, 6, 2, 5, 7, 1, 2, 6, 1, 3, 6, 10, 1, 3, 5, 1, 2, 3, 4, 5, 6, 8, 10, 1, 2, 3, 5, 6, 7, 10, 1, 2, 3, 7, 1, 2, 5, 1, 3, 4, 8, 4, 5, 1, 5, 6, 7, 2, 3, 7, 1, 2, 7, 9, 1, 2, 3, 7, 8, 1, 2, 3, 6, 7, 2, 3, 5, 8, 9, 3, 4, 5, 8, 9, 10, 2, 4, 6, 8, 9, 1, 2, 3, 5, 6, 7, 8, 9, 10, 1, 3, 8, 1, 2, 4, 6, 9, 3, 4, 7, 10, 1, 4, 6, 1, 2, 8, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 6, 7, 10, 1, 3, 4, 5, 6, 7, 9, 1, 2, 3, 6, 8, 3, 5, 8, 1, 3, 4, 5, 10, 1, 3, 4, 5, 6, 7, 9, 10, 1, 3, 5, 6, 7, 9, 10, 1, 2, 5, 1, 2, 3, 4, 5, 8, 9, 1, 5, 6, 7, 1, 2, 7, 1, 2, 3, 8, 10, 1, 3, 8, 10, 2, 5, 1, 2, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 8, 1, 3, 7, 8, 1, 3, 4, 5, 6, 8, 1, 7, 8, 9, 1, 4, 5, 1, 7, 3, 4, 5, 6, 7, 2, 3, 6, 7, 8, 1, 2, 3, 5, 6, 7, 8, 1, 2, 1, 3, 4, 5, 1, 3, 6, 1, 2, 3, 6, 10, 7, 10, 1, 4, 5, 1, 2, 3, 4, 6, 9, 10, 1, 2, 5, 8, 9, 10, 3, 4, 6, 8, 1, 2, 4, 6, 7, 1, 3, 5, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 5, 6, 8, 10, 1, 2, 3, 4, 5, 6, 8, 9, 10, 2, 4, 5, 9, 3, 5, 10, 1, 2, 3, 4, 5, 7, 10, 1, 2, 5, 6, 10, 1, 2, 3, 6, 4, 5, 2, 9, 1, 2, 3, 9, 1, 2, 7, 8, 1, 3, 5, 6, 7, 8, 2, 3, 5, 8, 10, 1, 4, 5, 9, 10, 1, 2, 4, 5, 1, 2, 6, 8, 1, 2, 4, 1, 2, 3, 4, 5, 1, 2, 4, 5, 6, 8, 10, 2, 5, 6, 1, 2, 3, 5, 8, 9, 10, 1, 4, 8, 1, 2, 4, 8, 10, 4, 7, 10, 3, 10, 1, 7, 8, 9, 1, 3, 9, 1, 4, 5, 9, 1, 2, 6, 8, 1, 2, 3, 4, 5, 6, 8, 9, 1, 2, 3, 4, 5, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 6, 8, 3, 5, 8, 1, 2, 3, 5, 6, 1, 3, 4, 6, 8, 9, 1, 4, 5, 6, 7, 9, 1, 5, 7, 8, 1, 3, 4, 5, 6, 7, 9, 10, 1, 2, 9, 1, 2, 4, 5, 9, 2, 3, 1, 2, 3, 7, 10, 1, 3, 4, 8, 9, 1, 2, 7, 8, 1, 2, 3, 7, 1, 3, 4, 10, 1, 2, 3, 5, 1, 3, 4, 5, 6, 9, 10, 2, 3, 8, 1, 4, 8, 9, 1, 3, 4, 3, 6, 7, 1, 4, 6, 9, 3, 4, 5, 8, 2, 7, 9, 1, 3, 7, 2, 6, 1, 3, 4, 7, 3, 4, 8, 1, 2, 3, 4, 5, 6, 7, 8, 10, 1, 5, 8, 10, 1, 2, 4, 2, 3, 5, 8, 10, 1, 2, 3, 4, 5, 7, 1, 2, 5, 7, 9], \"Freq\": [0.7717812028738013, 0.15435624057476025, 0.12260257964109535, 0.7356154778465721, 0.2597103249312062, 0.5194206498624124, 0.1298551624656031, 0.028333554876361702, 0.056667109752723405, 0.5100039877745106, 0.028333554876361702, 0.34000265851634043, 0.35580203575787, 0.23720135717191335, 0.35580203575787, 0.03953355952865222, 0.4952209060545828, 0.1650736353515276, 0.1650736353515276, 0.0825368176757638, 0.13411076423965343, 0.40233229271896026, 0.40233229271896026, 0.14811268795432458, 0.44433806386297375, 0.14811268795432458, 0.14811268795432458, 0.5261065648747464, 0.30063232278556934, 0.15031616139278467, 0.13106449178159624, 0.2621289835631925, 0.524257967126385, 0.6878040166210693, 0.17195100415526732, 0.049724125232030486, 0.3232068140081982, 0.12431031308007623, 0.09944825046406097, 0.2237585635441372, 0.07458618784804573, 0.049724125232030486, 0.024862062616015243, 0.024862062616015243, 0.09041496670635155, 0.1356224500595273, 0.09041496670635155, 0.09041496670635155, 0.04520748335317577, 0.5424898002381092, 0.17738678922265969, 0.3941928649392437, 0.11825785948177311, 0.07883857298784874, 0.07883857298784874, 0.05912892974088656, 0.03941928649392437, 0.03941928649392437, 0.019709643246962186, 0.13569694150003603, 0.18092925533338136, 0.04523231383334534, 0.27139388300007206, 0.09046462766669068, 0.09046462766669068, 0.2261615691667267, 0.4612086754205351, 0.34590650656540134, 0.11530216885513378, 0.15122738008040262, 0.6049095203216105, 0.15122738008040262, 0.07935958664230904, 0.5555171064961633, 0.05951968998173178, 0.03967979332115452, 0.11903937996346356, 0.07935958664230904, 0.03967979332115452, 0.1084299603416693, 0.1084299603416693, 0.6505797620500158, 0.21111943195213406, 0.6333582958564022, 0.30628136154428104, 0.4594220423164216, 0.15314068077214052, 0.20932879046685338, 0.5233219761671335, 0.20932879046685338, 0.08152044602335605, 0.40760223011678026, 0.24456133807006816, 0.1630408920467121, 0.06098615989695882, 0.07623269987119852, 0.06098615989695882, 0.04573961992271911, 0.09147923984543822, 0.24394463958783527, 0.04573961992271911, 0.2896842595105544, 0.04573961992271911, 0.06098615989695882, 0.3594101851040111, 0.2695576388280084, 0.2695576388280084, 0.5564713435621796, 0.03477945897263623, 0.03477945897263623, 0.24345621280845361, 0.1391178358905449, 0.04508573005795564, 0.18034292023182255, 0.18034292023182255, 0.5410287606954677, 0.04508573005795564, 0.39674532667930085, 0.06612422111321681, 0.39674532667930085, 0.13224844222643362, 0.40653842645688076, 0.26424997719697246, 0.10163460661422019, 0.040653842645688075, 0.040653842645688075, 0.06098076396853211, 0.06098076396853211, 0.48502121615736815, 0.48502121615736815, 0.2983718290744374, 0.11934873162977497, 0.2983718290744374, 0.23869746325954994, 0.02953200566122946, 0.41344807925721244, 0.08859601698368838, 0.3248520622735241, 0.05906401132245892, 0.02953200566122946, 0.02953200566122946, 0.1986029758725756, 0.23832357104709073, 0.1588823806980605, 0.23832357104709073, 0.03972059517451512, 0.07944119034903024, 0.21095789843072393, 0.42191579686144787, 0.21095789843072393, 0.04219157968614479, 0.12657473905843436, 0.14042055449604454, 0.07021027724802227, 0.2106308317440668, 0.5616822179841782, 0.26201978197943915, 0.5895445094537382, 0.13100989098971957, 0.44108248098043096, 0.0882164961960862, 0.44108248098043096, 0.45093448632158867, 0.45093448632158867, 0.17313331772824478, 0.17313331772824478, 0.17313331772824478, 0.34626663545648956, 0.6628344073746657, 0.04418896049164438, 0.2651337629498663, 0.042480269129068514, 0.08496053825813703, 0.25488161477441107, 0.5522434986778907, 0.20245020175521103, 0.05784291478720315, 0.6073506052656331, 0.1156858295744063, 0.5937557832682028, 0.23750231330728114, 0.6110020345421898, 0.3055010172710949, 0.21241664570869231, 0.21241664570869231, 0.42483329141738463, 0.10620832285434616, 0.1480653425893001, 0.2961306851786002, 0.1480653425893001, 0.2961306851786002, 0.1043247240409597, 0.15648708606143957, 0.1043247240409597, 0.4172988961638388, 0.1043247240409597, 0.29926304152044575, 0.17955782491226743, 0.17955782491226743, 0.29926304152044575, 0.26984788339953286, 0.053969576679906574, 0.053969576679906574, 0.053969576679906574, 0.10793915335981315, 0.26984788339953286, 0.10793915335981315, 0.20906078431252123, 0.10453039215626062, 0.522651960781303, 0.10453039215626062, 0.18484962539998218, 0.06161654179999406, 0.4313157925999584, 0.18484962539998218, 0.06161654179999406, 0.06161654179999406, 0.18096982896582708, 0.5429094868974812, 0.09048491448291354, 0.04524245724145677, 0.09048491448291354, 0.06642338358130878, 0.19927015074392634, 0.2656935343252351, 0.3985403014878527, 0.19403191939970477, 0.29104787909955715, 0.29104787909955715, 0.19403191939970477, 0.750261372035323, 0.21436039201009227, 0.22789391140453708, 0.30385854853938277, 0.37982318567422846, 0.20250961692201713, 0.08100384676880686, 0.3240153870752274, 0.3240153870752274, 0.04050192338440343, 0.31060987591756495, 0.05176831265292749, 0.46591481387634737, 0.10353662530585497, 0.5110180879304944, 0.2555090439652472, 0.2235704134695913, 0.13111483396378032, 0.39334450189134096, 0.26222966792756064, 0.13111483396378032, 0.05451549653709524, 0.4906394688338572, 0.1635464896112857, 0.10903099307419048, 0.1635464896112857, 0.5312830592831012, 0.3187698355698607, 0.05312830592831012, 0.07340082611873984, 0.29360330447495936, 0.48933884079159895, 0.024466942039579945, 0.024466942039579945, 0.07340082611873984, 0.40049719453824395, 0.26699812969216263, 0.13349906484608132, 0.26699812969216263, 0.21342916907692358, 0.12195952518681348, 0.15244940648351685, 0.21342916907692358, 0.06097976259340674, 0.21342916907692358, 0.15139315580013693, 0.30278631160027386, 0.15139315580013693, 0.30278631160027386, 0.17629029214598166, 0.17629029214598166, 0.3525805842919633, 0.17629029214598166, 0.2785425536133611, 0.0397917933733373, 0.0795835867466746, 0.11937538012001189, 0.0795835867466746, 0.1591671734933492, 0.1989589668666865, 0.0397917933733373, 0.34916168987411395, 0.34916168987411395, 0.17458084493705697, 0.6814995319709533, 0.1703748829927383, 0.11633860761428329, 0.11633860761428329, 0.40718512664999146, 0.23267721522856658, 0.058169303807141644, 0.10503760340423093, 0.7352632238296165, 0.10503760340423093, 0.1704075230012748, 0.3164711141452246, 0.19475145485859977, 0.07303179557197491, 0.04868786371464994, 0.04868786371464994, 0.04868786371464994, 0.04868786371464994, 0.02434393185732497, 0.02434393185732497, 0.06355578162077959, 0.11122261783636428, 0.11122261783636428, 0.34955679891428776, 0.06355578162077959, 0.03177789081038979, 0.03177789081038979, 0.07944472702597448, 0.11122261783636428, 0.04766683621558469, 0.13253742080937325, 0.06626871040468663, 0.13253742080937325, 0.5964183936421796, 0.1060921821145402, 0.2576524422781691, 0.07578013008181443, 0.2121843642290804, 0.09093615609817732, 0.060624104065451545, 0.07578013008181443, 0.030312052032725773, 0.030312052032725773, 0.04546807804908866, 0.17943631979521427, 0.35887263959042853, 0.35887263959042853, 0.0973004314922065, 0.194600862984413, 0.0973004314922065, 0.194600862984413, 0.0973004314922065, 0.194600862984413, 0.13186180879177256, 0.3955854263753177, 0.13186180879177256, 0.2637236175835451, 0.31587387153984914, 0.10529129051328305, 0.31587387153984914, 0.10529129051328305, 0.26689291798849807, 0.4003393769827471, 0.13344645899424903, 0.13344645899424903, 0.09006079698929953, 0.2701823909678986, 0.18012159397859906, 0.2701823909678986, 0.09006079698929953, 0.26428653665016477, 0.13214326832508239, 0.13214326832508239, 0.26428653665016477, 0.09970776376845235, 0.09970776376845235, 0.29912329130535703, 0.46530289758611093, 0.03323592125615078, 0.4545587314088083, 0.06993211252443204, 0.1748302813110801, 0.20979633757329613, 0.06993211252443204, 0.547198421557603, 0.3077991121261517, 0.06839980269470038, 0.06839980269470038, 0.35867942508085937, 0.08277217501865985, 0.1655443500373197, 0.2759072500621995, 0.02759072500621995, 0.0551814500124399, 0.25523026691256917, 0.638075667281423, 0.07910382148291194, 0.7119343933462075, 0.07910382148291194, 0.07910382148291194, 0.6857701056543356, 0.08572126320679195, 0.08572126320679195, 0.08572126320679195, 0.17487818515419618, 0.17487818515419618, 0.34975637030839235, 0.17487818515419618, 0.35318757999607675, 0.11772919333202558, 0.41205217666208954, 0.05886459666601279, 0.05886459666601279, 0.09373952019323602, 0.04686976009661801, 0.14060928028985403, 0.6093068812560342, 0.09373952019323602, 0.05825184892532499, 0.46601479140259994, 0.05825184892532499, 0.11650369785064998, 0.23300739570129997, 0.05825184892532499, 0.07249377334600471, 0.07249377334600471, 0.14498754669200942, 0.07249377334600471, 0.6524439601140424, 0.1964355459947178, 0.6384155244828328, 0.04910888649867945, 0.04910888649867945, 0.04910888649867945, 0.1692984309395971, 0.1692984309395971, 0.5925445082885898, 0.106928734496983, 0.427714937987932, 0.0534643672484915, 0.320786203490949, 0.106928734496983, 0.5944412953366687, 0.06604903281518541, 0.06604903281518541, 0.19814709844555622, 0.5191096231926892, 0.18876713570643242, 0.047191783926608104, 0.23595891963304053, 0.6755380016942009, 0.13510760033884017, 0.5346524075143454, 0.17821746917144848, 0.35643493834289697, 0.15953245136977012, 0.2392986770546552, 0.5583635797941955, 0.3099623599030484, 0.1549811799515242, 0.4649435398545726, 0.7509540625882255, 0.21455830359663586, 0.1794408664328643, 0.1794408664328643, 0.3588817328657286, 0.1794408664328643, 0.11081605454520094, 0.1662240818178014, 0.05540802727260047, 0.27704013636300234, 0.11081605454520094, 0.22163210909040187, 0.05540802727260047, 0.3530913232396404, 0.42370958788756846, 0.07061826464792807, 0.07061826464792807, 0.39151351509405985, 0.2610090100627066, 0.2610090100627066, 0.27189499602837447, 0.4758162430496553, 0.06797374900709362, 0.045315832671395745, 0.045315832671395745, 0.045315832671395745, 0.022657916335697872, 0.31840867807937007, 0.08980757586854028, 0.02449297523687462, 0.016328650157916413, 0.02449297523687462, 0.31024435300041187, 0.14695785142124773, 0.008164325078958206, 0.05715027555270745, 0.016328650157916413, 0.11857789927495678, 0.11857789927495678, 0.23715579854991356, 0.11857789927495678, 0.23715579854991356, 0.4273048199551005, 0.32047861496632535, 0.10682620498877513, 0.2040674866819208, 0.4081349733638416, 0.17005623890160068, 0.2040674866819208, 0.08687830333632127, 0.08687830333632127, 0.17375660667264253, 0.08687830333632127, 0.5212698200179275, 0.3472766530904328, 0.3472766530904328, 0.1736383265452164, 0.08710905832743092, 0.39199076247343917, 0.08710905832743092, 0.08710905832743092, 0.1306635874911464, 0.1306635874911464, 0.5101665650057867, 0.40813325200462935, 0.15235180901655695, 0.3047036180331139, 0.15235180901655695, 0.15235180901655695, 0.27723589265996207, 0.2310299105499684, 0.09241196421998736, 0.36964785687994944, 0.1760960639001861, 0.3521921278003722, 0.1760960639001861, 0.08804803195009304, 0.08804803195009304, 0.08804803195009304, 0.3857709166708933, 0.15430836666835732, 0.07715418333417866, 0.07715418333417866, 0.231462550002536, 0.4776297061184223, 0.05970371326480279, 0.05970371326480279, 0.17911113979440837, 0.17911113979440837, 0.4457415994174654, 0.13715126135922012, 0.41145378407766037, 0.2612539667971519, 0.15675238007829115, 0.10450158671886076, 0.15675238007829115, 0.05225079335943038, 0.2612539667971519, 0.2772709218604175, 0.22181673748833403, 0.11090836874416701, 0.332725106232501, 0.2703225234886579, 0.4054837852329868, 0.2703225234886579, 0.31408627405547906, 0.21986039183883532, 0.18845176443328743, 0.18845176443328743, 0.0628172548110958, 0.31989217624742494, 0.10663072541580831, 0.21326145083161663, 0.10663072541580831, 0.21326145083161663, 0.02901237131486931, 0.08703711394460793, 0.08703711394460793, 0.08703711394460793, 0.2901237131486931, 0.11604948525947724, 0.08703711394460793, 0.14506185657434656, 0.05802474262973862, 0.2967734926139335, 0.05935469852278669, 0.05935469852278669, 0.1780640955683601, 0.2967734926139335, 0.05935469852278669, 0.2903429871768002, 0.39922160736810025, 0.03629287339710002, 0.03629287339710002, 0.03629287339710002, 0.10887862019130007, 0.07258574679420005, 0.14506754559719579, 0.21760131839579366, 0.036266886399298946, 0.29013509119439157, 0.14506754559719579, 0.10880065919789683, 0.2920135427348668, 0.2920135427348668, 0.2920135427348668, 0.08876900774282002, 0.3550760309712801, 0.26630702322846006, 0.26630702322846006, 0.4898309659428638, 0.01959323863771455, 0.0391864772754291, 0.09796619318857276, 0.0391864772754291, 0.23511886365257462, 0.0391864772754291, 0.14876842272089963, 0.5206894795231487, 0.07438421136044981, 0.14876842272089963, 0.10475194043994442, 0.20950388087988883, 0.6285116426396665, 0.036804637021590265, 0.36804637021590264, 0.25763245915113187, 0.036804637021590265, 0.18402318510795132, 0.07360927404318053, 0.5382337144587631, 0.17941123815292104, 0.17941123815292104, 0.024032885372331603, 0.016021923581554402, 0.1682301976063212, 0.19226308297865283, 0.080109617907772, 0.25635077730487044, 0.20027404476943, 0.056076732535440404, 0.0872516583106408, 0.436258291553204, 0.2617549749319224, 0.0872516583106408, 0.39289129748530965, 0.0561273282121871, 0.1683819846365613, 0.2806366410609355, 0.0561273282121871, 0.0561273282121871, 0.47709709551213453, 0.23854854775606726, 0.11927427387803363, 0.11927427387803363, 0.350989552483463, 0.23399303498897533, 0.23399303498897533, 0.09459863599519032, 0.3783945439807613, 0.3783945439807613, 0.09459863599519032, 0.035672104829321136, 0.21403262897592681, 0.14268841931728454, 0.32104894346389024, 0.24970473380524796, 0.26584001512096356, 0.26584001512096356, 0.26584001512096356, 0.1993800113407227, 0.09530388011708958, 0.3812155204683583, 0.3812155204683583, 0.29158725831750787, 0.09719575277250263, 0.29158725831750787, 0.19439150554500526, 0.2635374496617038, 0.052707489932340756, 0.15812246979702227, 0.10541497986468151, 0.2635374496617038, 0.15812246979702227, 0.3456824882731573, 0.3456824882731573, 0.17284124413657864, 0.1827327950007172, 0.2284159937508965, 0.0456831987501793, 0.31978239125125507, 0.0456831987501793, 0.0456831987501793, 0.0456831987501793, 0.0456831987501793, 0.2767712043668988, 0.4305329845707314, 0.06150471208153306, 0.06150471208153306, 0.06150471208153306, 0.0922570681222996, 0.7310175374950701, 0.13053884598126253, 0.05221553839250501, 0.026107769196252507, 0.026107769196252507, 0.026107769196252507, 0.2798035561228431, 0.023316963010236922, 0.1165848150511846, 0.06995088903071077, 0.046633926020473844, 0.13990177806142154, 0.13990177806142154, 0.16321874107165846, 0.18146133026685482, 0.18146133026685482, 0.5443839908005644, 0.39280331344366526, 0.1309344378145551, 0.2618688756291102, 0.1279994771592337, 0.7679968629554024, 0.14911584574869965, 0.14911584574869965, 0.14911584574869965, 0.07455792287434983, 0.07455792287434983, 0.3727896143717491, 0.03129314299333677, 0.4224574304100464, 0.14081914347001548, 0.07823285748334192, 0.18775885796002062, 0.06258628598667354, 0.03129314299333677, 0.03129314299333677, 0.5741471361621139, 0.28707356808105694, 0.05741471361621139, 0.16304964311556772, 0.16304964311556772, 0.16304964311556772, 0.4891489293467031, 0.5445379642573616, 0.40840347319302117, 0.23410185695705263, 0.46820371391410526, 0.11705092847852631, 0.11705092847852631, 0.3564022593684248, 0.07128045187368497, 0.07128045187368497, 0.28512180749473987, 0.14256090374736993, 0.45398127793908394, 0.30265418529272264, 0.15132709264636132, 0.11635985955970864, 0.5817992977985432, 0.11635985955970864, 0.11635985955970864, 0.17199497690629928, 0.049141421973228364, 0.4177020867724411, 0.24570710986614183, 0.024570710986614182, 0.07371213295984255, 0.3090312023530433, 0.185418721411826, 0.06180624047060867, 0.12361248094121734, 0.06180624047060867, 0.3090312023530433, 0.4623879379586794, 0.30825862530578624, 0.15412931265289312, 0.06696068130237325, 0.3013230658606796, 0.08370085162796656, 0.20088204390711972, 0.01674017032559331, 0.03348034065118662, 0.08370085162796656, 0.21762221423271305, 0.35715153280713025, 0.35715153280713025, 0.3637106707640781, 0.41566933801608924, 0.10391733450402231, 0.051958667252011155, 0.051958667252011155, 0.3187709323298865, 0.1062569774432955, 0.425027909773182, 0.6159449350172986, 0.10265748916954977, 0.10265748916954977, 0.10265748916954977, 0.11821037558233696, 0.11821037558233696, 0.23642075116467393, 0.3546311267470109, 0.30876744021403296, 0.10292248007134433, 0.30876744021403296, 0.20584496014268866, 0.10292248007134433, 0.35315677358055964, 0.17657838679027982, 0.35315677358055964, 0.07806413392129148, 0.05204275594752765, 0.13010688986881913, 0.27322446872452016, 0.27322446872452016, 0.06505344493440957, 0.11709620088193722, 0.5191304422589242, 0.12978261056473106, 0.12978261056473106, 0.17357738605455653, 0.5207321581636696, 0.17357738605455653, 0.149635216771797, 0.448905650315391, 0.299270433543594, 0.17430415175878083, 0.34860830351756167, 0.34860830351756167, 0.4993131398165614, 0.08321885663609357, 0.08321885663609357, 0.2496565699082807, 0.2073190225586405, 0.13821268170576032, 0.6219570676759214, 0.1171255670988789, 0.17568835064831836, 0.19032904653567823, 0.21961043831039795, 0.014640695887359863, 0.014640695887359863, 0.2049697424230381, 0.04392208766207959, 0.10815497941688142, 0.32446493825064426, 0.1802582990281357, 0.07210331961125428, 0.25236161863939, 0.03605165980562714, 0.03605165980562714, 0.13158601786372065, 0.39475805359116195, 0.13158601786372065, 0.2631720357274413, 0.4667145921158424, 0.35003594408688177, 0.1166786480289606, 0.4862001137178344, 0.19448004548713377, 0.09724002274356688, 0.09724002274356688, 0.3086371386240478, 0.6172742772480956, 0.0964291321707118, 0.1928582643414236, 0.5785747930242708, 0.0964291321707118, 0.27346361594763624, 0.656312678274327, 0.054692723189527254, 0.30006962189820535, 0.30006962189820535, 0.07501740547455134, 0.22505221642365403, 0.37921400839365277, 0.18960700419682638, 0.22752840503619168, 0.11376420251809584, 0.03792140083936528, 0.1830528175232084, 0.5491584525696251, 0.06101760584106946, 0.06101760584106946, 0.06101760584106946, 0.1158670792603156, 0.4634683170412624, 0.1158670792603156, 0.1158670792603156, 0.1158670792603156, 0.17542217404229501, 0.08771108702114751, 0.17542217404229501, 0.08771108702114751, 0.26313326106344254, 0.08771108702114751, 0.31307535972405476, 0.10435845324135158, 0.10435845324135158, 0.10435845324135158, 0.31307535972405476, 0.16938290096442704, 0.3500579953264826, 0.1467985141691701, 0.045168773590513876, 0.022584386795256938, 0.045168773590513876, 0.12421412737391316, 0.033876580192885405, 0.06775316038577081, 0.11791133977384202, 0.5895566988692101, 0.23582267954768404, 0.22436273956845643, 0.22436273956845643, 0.07478757985615214, 0.07478757985615214, 0.29915031942460857, 0.597567253172974, 0.2109060893551673, 0.07030202978505577, 0.10545304467758365, 0.17642603836827656, 0.3528520767365531, 0.3528520767365531, 0.14805734346405516, 0.5922293738562207, 0.14805734346405516, 0.24204800228457082, 0.20977493531329472, 0.20977493531329472, 0.09681920091382833, 0.03227306697127611, 0.016136533485638056, 0.04840960045691416, 0.016136533485638056, 0.12909226788510444, 0.362273988308709, 0.241515992205806, 0.0603789980514515, 0.3018949902572575, 0.3761039903899281, 0.10257381556088949, 0.13676508741451932, 0.10257381556088949, 0.10257381556088949, 0.06838254370725966, 0.10257381556088949, 0.09676198377121434, 0.19352396754242868, 0.09676198377121434, 0.19352396754242868, 0.38704793508485735, 0.0537787367739703, 0.1613362103219109, 0.7529023148355841, 0.08132918273067072, 0.08132918273067072, 0.08132918273067072, 0.4066459136533536, 0.24398754819201218, 0.029164542701132945, 0.014582271350566473, 0.1604049848562312, 0.1604049848562312, 0.014582271350566473, 0.08749362810339884, 0.04374681405169942, 0.4666326832181271, 0.0885086137140482, 0.0885086137140482, 0.2655258411421446, 0.0885086137140482, 0.2655258411421446, 0.0885086137140482, 0.0885086137140482, 0.113695417612444, 0.341086252837332, 0.5684770880622201, 0.14269222884463212, 0.14269222884463212, 0.14269222884463212, 0.19025630512617614, 0.047564076281544035, 0.047564076281544035, 0.28538445768926424, 0.5955769180964594, 0.11911538361929187, 0.11911538361929187, 0.11911538361929187, 0.29612361626425693, 0.5922472325285139, 0.07403090406606423, 0.34832332267427407, 0.45717436100998476, 0.1306212460028528, 0.04354041533428426, 0.02177020766714213, 0.5150765059570687, 0.10301530119141374, 0.30904590357424117, 0.05150765059570687, 0.34222321880710255, 0.5133348282106538, 0.2073251432265312, 0.45611531509836867, 0.12439508593591873, 0.08293005729061248, 0.04146502864530624, 0.04146502864530624, 0.31841235087941205, 0.21227490058627468, 0.08490996023450988, 0.06368247017588241, 0.04245498011725494, 0.04245498011725494, 0.16981992046901975, 0.04245498011725494, 0.06611697013353275, 0.7272866714688602, 0.1322339402670655, 0.06611697013353275, 0.19187102700170433, 0.4317098107538348, 0.14390327025127825, 0.04796775675042608, 0.09593551350085217, 0.04796775675042608, 0.4170425962193554, 0.04633806624659505, 0.0926761324931901, 0.4170425962193554, 0.6782018603047122, 0.09688598004353031, 0.19377196008706063, 0.7221357400122217, 0.12035595666870362, 0.5780922156885558, 0.05255383778986872, 0.10510767557973744, 0.10510767557973744, 0.10510767557973744, 0.5187613859382779, 0.14821753883950797, 0.07410876941975399, 0.07410876941975399, 0.14821753883950797, 0.18491478245531653, 0.5547443473659496, 0.11094886947318991, 0.036982956491063305, 0.036982956491063305, 0.036982956491063305, 0.036982956491063305, 0.3196738173944786, 0.5594291804403375, 0.16142124482880765, 0.48426373448642296, 0.08071062241440383, 0.16142124482880765, 0.23492864854624973, 0.46985729709249946, 0.23492864854624973, 0.06589911874461653, 0.2635964749784661, 0.19769735623384957, 0.2635964749784661, 0.19769735623384957, 0.3400142733076273, 0.5950249782883478, 0.4414596631182256, 0.3531677304945805, 0.08829193262364513, 0.1329452832288545, 0.06647264161442724, 0.06647264161442724, 0.3323632080721362, 0.06647264161442724, 0.06647264161442724, 0.19941792484328175, 0.11540611548227128, 0.23081223096454256, 0.4327729330585173, 0.11540611548227128, 0.02885152887056782, 0.05770305774113564, 0.2647673711025284, 0.1323836855512642, 0.39715105665379263, 0.1323836855512642, 0.16334822680864283, 0.24502234021296426, 0.16334822680864283, 0.08167411340432142, 0.24502234021296426, 0.21631604458451176, 0.10815802229225588, 0.10815802229225588, 0.4326320891690235, 0.12089809592217078, 0.3905938483639364, 0.0371994141298987, 0.11159824238969611, 0.009299853532474676, 0.13949780298712014, 0.009299853532474676, 0.10229838885722144, 0.08369868179227208, 0.48055666184449997, 0.05339518464938889, 0.16018555394816666, 0.05339518464938889, 0.05339518464938889, 0.10679036929877778, 0.05339518464938889, 0.10467501722122988, 0.13084377152653734, 0.02616875430530747, 0.0785062629159224, 0.3140250516636896, 0.1831812801371523, 0.02616875430530747, 0.0785062629159224, 0.10467501722122988, 0.7534549427341697, 0.03275891055365955, 0.0655178211073191, 0.1310356422146382, 0.6428692929303036, 0.1753279889809919, 0.1461066574841599, 0.10882262136391377, 0.07254841424260917, 0.3990162783343505, 0.12695972492456606, 0.12695972492456606, 0.12695972492456606, 0.018137103560652294, 0.10584390631961996, 0.10584390631961996, 0.21168781263923991, 0.3175317189588599, 0.21168781263923991, 0.10562030657066833, 0.10562030657066833, 0.21124061314133666, 0.5281015328533416, 0.11392171774326569, 0.7974520242028599, 0.6801636607540561, 0.22672122025135205, 0.19616659432253736, 0.13077772954835823, 0.06538886477417911, 0.5231109181934329, 0.26787730443501906, 0.26787730443501906, 0.26787730443501906, 0.13393865221750953, 0.35409481943168475, 0.22533306691107213, 0.19314262878091895, 0.09657131439045948, 0.09657131439045948, 0.03219043813015316, 0.03249356849345237, 0.03249356849345237, 0.6498713698690474, 0.22745497945416657, 0.03249356849345237, 0.2092481771211618, 0.0697493923737206, 0.48824574661604425, 0.0697493923737206, 0.0697493923737206, 0.1723785316100571, 0.08618926580502854, 0.08618926580502854, 0.6033248606351997, 0.15177427691886577, 0.30354855383773155, 0.15177427691886577, 0.30354855383773155, 0.35041535727718404, 0.17520767863859202, 0.35041535727718404, 0.061442399144669965, 0.061442399144669965, 0.6758663905913697, 0.12288479828933993, 0.061442399144669965, 0.037446299669883124, 0.3744629966988312, 0.07489259933976625, 0.07489259933976625, 0.1497851986795325, 0.2621240976891819, 0.037446299669883124, 0.3947053404101017, 0.3947053404101017, 0.23682320424606101, 0.08598721326310037, 0.17197442652620074, 0.08598721326310037, 0.057324808842066914, 0.2006368309472342, 0.2006368309472342, 0.17197442652620074, 0.3562321299899977, 0.3562321299899977, 0.3562321299899977, 0.10329268485690363, 0.5164634242845182, 0.2582317121422591, 0.051646342428451814, 0.051646342428451814, 0.2691388189188254, 0.4037082283782381, 0.1345694094594127, 0.3612752936857584, 0.602125489476264, 0.3608605258943072, 0.0902151314735768, 0.3608605258943072, 0.0902151314735768, 0.6102306401402702, 0.11441824502630066, 0.22883649005260132, 0.1035053293466378, 0.1035053293466378, 0.5175266467331889, 0.2070106586932756, 0.15215394994762824, 0.15215394994762824, 0.3043078998952565, 0.3043078998952565, 0.05011365832046212, 0.5011365832046212, 0.02505682916023106, 0.15034097496138635, 0.07517048748069317, 0.05011365832046212, 0.02505682916023106, 0.1252841458011553, 0.04516028241438311, 0.45160282414383107, 0.04516028241438311, 0.09032056482876621, 0.13548084724314932, 0.18064112965753243, 0.3483814155192682, 0.32788839107695833, 0.054648065179493055, 0.054648065179493055, 0.054648065179493055, 0.03415504073718316, 0.08197209776923958, 0.027324032589746527, 0.006831008147436632, 0.013662016294873264, 0.7506103112342302, 0.0326352309232274, 0.163176154616137, 0.0326352309232274, 0.2896586132376436, 0.19310574215842904, 0.4827643553960726, 0.09481871944644267, 0.284456158339328, 0.18963743889288534, 0.09481871944644267, 0.3792748777857707, 0.19257949100865748, 0.04814487275216437, 0.19257949100865748, 0.19257949100865748, 0.09628974550432874, 0.24072436376082185, 0.08695895793954628, 0.5000140081523912, 0.17391791587909256, 0.06521921845465971, 0.02173973948488657, 0.13043843690931942, 0.2654827452994075, 0.3982241179491113, 0.13274137264970376, 0.13274137264970376, 0.13172286364075692, 0.11525750568566231, 0.46103002274264926, 0.11525750568566231, 0.016465357955094614, 0.13172286364075692, 0.016465357955094614, 0.016465357955094614, 0.17236233704879997, 0.5170870111464, 0.17236233704879997, 0.08687789696293184, 0.08687789696293184, 0.17375579392586368, 0.08687789696293184, 0.521267381777591, 0.38839446377021825, 0.5178592850269577, 0.08224921523599778, 0.08224921523599778, 0.4112460761799889, 0.3289968609439911, 0.04112460761799889, 0.4897309172650053, 0.06678148871795526, 0.24486545863250264, 0.15582347367522895, 0.04452099247863685, 0.21353703304432695, 0.32030554956649043, 0.32030554956649043, 0.10676851652216347, 0.2763378220561474, 0.5526756441122948, 0.06908445551403684, 0.06908445551403684, 0.1764014877222817, 0.1764014877222817, 0.3528029754445634, 0.1764014877222817, 0.1467000985878555, 0.4767753204105303, 0.07335004929392774, 0.293400197175711, 0.41827906056420167, 0.11407610742660046, 0.0760507382844003, 0.0760507382844003, 0.19012684571100075, 0.03802536914220015, 0.03802536914220015, 0.6865668430260655, 0.06865668430260655, 0.20597005290781964, 0.22718527353635337, 0.1514568490242356, 0.22718527353635337, 0.378642122560589, 0.08073230867834168, 0.4036615433917084, 0.4036615433917084, 0.3053169947392195, 0.3053169947392195, 0.3053169947392195, 0.0752052382950533, 0.1504104765901066, 0.3008209531802132, 0.45123142977031977, 0.17551120772382783, 0.08775560386191392, 0.35102241544765567, 0.35102241544765567, 0.7833403177204442, 0.07833403177204441, 0.07833403177204441, 0.3595259941564376, 0.23968399610429175, 0.3595259941564376, 0.2213482942221656, 0.7193819562220382, 0.15085731381007336, 0.6034292552402934, 0.07542865690503668, 0.07542865690503668, 0.37391717229584737, 0.5234840412141863, 0.07478343445916948, 0.29242611138759317, 0.10633676777730659, 0.013292095972163324, 0.06646047986081663, 0.14621305569379658, 0.13292095972163326, 0.053168383888653296, 0.13292095972163326, 0.053168383888653296, 0.06782275387917361, 0.06782275387917361, 0.7460502926709096, 0.06782275387917361, 0.6066996431839632, 0.1516749107959908, 0.1516749107959908, 0.3939055315366543, 0.3376333127457037, 0.056272218790950616, 0.028136109395475308, 0.14068054697737653, 0.06102253235053753, 0.2440901294021501, 0.12204506470107505, 0.36613519410322515, 0.12204506470107505, 0.06102253235053753, 0.31799455983100133, 0.21199637322066753, 0.05299909330516688, 0.21199637322066753, 0.15899727991550067], \"Term\": [\"ability\", \"ability\", \"abstract\", \"abstract\", \"academic\", \"academic\", \"academic\", \"accounting\", \"accounting\", \"accounting\", \"accounting\", \"accounting\", \"activity\", \"activity\", \"activity\", \"activity\", \"actor\", \"actor\", \"actor\", \"actor\", \"addition\", \"addition\", \"addition\", \"address\", \"address\", \"address\", \"address\", \"adoption\", \"adoption\", \"adoption\", \"agenda\", \"agenda\", \"agenda\", \"aim\", \"aim\", \"analysis\", \"analysis\", \"analysis\", \"analysis\", \"analysis\", \"analysis\", \"analysis\", \"analysis\", \"analysis\", \"application\", \"application\", \"application\", \"application\", \"application\", \"application\", \"approach\", \"approach\", \"approach\", \"approach\", \"approach\", \"approach\", \"approach\", \"approach\", \"approach\", \"article\", \"article\", \"article\", \"article\", \"article\", \"article\", \"article\", \"assessment\", \"assessment\", \"assessment\", \"attention\", \"attention\", \"attention\", \"author\", \"author\", \"author\", \"author\", \"author\", \"author\", \"author\", \"available\", \"available\", \"available\", \"balance\", \"balance\", \"behavior\", \"behavior\", \"behavior\", \"benefit\", \"benefit\", \"benefit\", \"book\", \"book\", \"book\", \"book\", \"business\", \"business\", \"business\", \"business\", \"business\", \"business\", \"business\", \"business\", \"business\", \"business\", \"buyer\", \"buyer\", \"buyer\", \"capability\", \"capability\", \"capability\", \"capability\", \"capability\", \"capacity\", \"capacity\", \"capacity\", \"capacity\", \"capacity\", \"capital\", \"capital\", \"capital\", \"capital\", \"case\", \"case\", \"case\", \"case\", \"case\", \"case\", \"case\", \"central\", \"central\", \"chain\", \"chain\", \"chain\", \"chain\", \"challenge\", \"challenge\", \"challenge\", \"challenge\", \"challenge\", \"challenge\", \"challenge\", \"change\", \"change\", \"change\", \"change\", \"change\", \"change\", \"chapter\", \"chapter\", \"chapter\", \"chapter\", \"chapter\", \"characteristic\", \"characteristic\", \"characteristic\", \"characteristic\", \"china\", \"china\", \"china\", \"choice\", \"choice\", \"choice\", \"christian\", \"christian\", \"clean\", \"clean\", \"clean\", \"clean\", \"collaboration\", \"collaboration\", \"collaboration\", \"collaborative\", \"collaborative\", \"collaborative\", \"collaborative\", \"company\", \"company\", \"company\", \"company\", \"competition\", \"competition\", \"complex\", \"complex\", \"component\", \"component\", \"component\", \"component\", \"comprehensive\", \"comprehensive\", \"comprehensive\", \"comprehensive\", \"concept\", \"concept\", \"concept\", \"concept\", \"concept\", \"conceptual\", \"conceptual\", \"conceptual\", \"conceptual\", \"condition\", \"condition\", \"condition\", \"condition\", \"condition\", \"condition\", \"condition\", \"consequence\", \"consequence\", \"consequence\", \"consequence\", \"consumption\", \"consumption\", \"consumption\", \"consumption\", \"consumption\", \"consumption\", \"context\", \"context\", \"context\", \"context\", \"context\", \"contribution\", \"contribution\", \"contribution\", \"contribution\", \"control\", \"control\", \"control\", \"control\", \"corporate\", \"corporate\", \"cost\", \"cost\", \"cost\", \"country\", \"country\", \"country\", \"country\", \"country\", \"creation\", \"creation\", \"creation\", \"creation\", \"critical\", \"critical\", \"critical\", \"crucial\", \"crucial\", \"crucial\", \"crucial\", \"current\", \"current\", \"current\", \"current\", \"current\", \"customer\", \"customer\", \"customer\", \"danish\", \"danish\", \"danish\", \"danish\", \"danish\", \"danish\", \"data\", \"data\", \"data\", \"data\", \"datum\", \"datum\", \"datum\", \"datum\", \"datum\", \"datum\", \"debate\", \"debate\", \"debate\", \"debate\", \"decade\", \"decade\", \"decade\", \"decade\", \"decision\", \"decision\", \"decision\", \"decision\", \"decision\", \"decision\", \"decision\", \"decision\", \"demand\", \"demand\", \"demand\", \"demonstrate\", \"demonstrate\", \"denmark\", \"denmark\", \"denmark\", \"denmark\", \"denmark\", \"department\", \"department\", \"department\", \"design\", \"design\", \"design\", \"design\", \"design\", \"design\", \"design\", \"design\", \"design\", \"design\", \"development\", \"development\", \"development\", \"development\", \"development\", \"development\", \"development\", \"development\", \"development\", \"development\", \"difference\", \"difference\", \"difference\", \"difference\", \"different\", \"different\", \"different\", \"different\", \"different\", \"different\", \"different\", \"different\", \"different\", \"different\", \"difficult\", \"difficult\", \"difficult\", \"dimension\", \"dimension\", \"dimension\", \"dimension\", \"dimension\", \"dimension\", \"direction\", \"direction\", \"direction\", \"direction\", \"discussion\", \"discussion\", \"discussion\", \"discussion\", \"driver\", \"driver\", \"driver\", \"driver\", \"dynamic\", \"dynamic\", \"dynamic\", \"dynamic\", \"dynamic\", \"early\", \"early\", \"early\", \"early\", \"economic\", \"economic\", \"economic\", \"economic\", \"economic\", \"economy\", \"economy\", \"economy\", \"economy\", \"economy\", \"ecosystem\", \"ecosystem\", \"ecosystem\", \"ecosystem\", \"effect\", \"effect\", \"effect\", \"effect\", \"effect\", \"effect\", \"effective\", \"effective\", \"effort\", \"effort\", \"effort\", \"effort\", \"emerald\", \"emerald\", \"emerald\", \"emerald\", \"emergence\", \"emergence\", \"emergence\", \"emergence\", \"employee\", \"employee\", \"employee\", \"employee\", \"employee\", \"energy\", \"energy\", \"energy\", \"energy\", \"energy\", \"enterprise\", \"enterprise\", \"enterprise\", \"enterprise\", \"enterprise\", \"enterprise\", \"entrepreneur\", \"entrepreneur\", \"entrepreneur\", \"entrepreneur\", \"entrepreneur\", \"entrepreneurial\", \"entrepreneurial\", \"entrepreneurial\", \"entrepreneurial\", \"entrepreneurial\", \"entrepreneurship\", \"entrepreneurship\", \"entrepreneurship\", \"environmental\", \"environmental\", \"environmental\", \"environmental\", \"environmental\", \"european\", \"european\", \"european\", \"european\", \"evidence\", \"evidence\", \"evidence\", \"evidence\", \"evolution\", \"evolution\", \"examine\", \"examine\", \"examine\", \"example\", \"example\", \"example\", \"exclusive\", \"exclusive\", \"exclusive\", \"experience\", \"experience\", \"external\", \"external\", \"external\", \"external\", \"factor\", \"factor\", \"factor\", \"factor\", \"factor\", \"factor\", \"factor\", \"failure\", \"failure\", \"failure\", \"failure\", \"finally\", \"finally\", \"finally\", \"finding\", \"finding\", \"finding\", \"finding\", \"finding\", \"finding\", \"finding\", \"firm\", \"firm\", \"firm\", \"firm\", \"firm\", \"firm\", \"firm\", \"firm\", \"firm\", \"firm\", \"focus\", \"focus\", \"focus\", \"focus\", \"focus\", \"foundation\", \"foundation\", \"foundation\", \"framework\", \"framework\", \"framework\", \"framework\", \"francis\", \"francis\", \"francis\", \"francis\", \"francis\", \"function\", \"function\", \"function\", \"future\", \"future\", \"future\", \"future\", \"future\", \"future\", \"gap\", \"gap\", \"general\", \"general\", \"general\", \"general\", \"global\", \"global\", \"global\", \"global\", \"goal\", \"goal\", \"goal\", \"goal\", \"goal\", \"goal\", \"governance\", \"governance\", \"governance\", \"governance\", \"governance\", \"government\", \"government\", \"government\", \"government\", \"government\", \"green\", \"green\", \"green\", \"group\", \"group\", \"group\", \"group\", \"group\", \"group\", \"growth\", \"growth\", \"growth\", \"growth\", \"hand\", \"hand\", \"hand\", \"high\", \"high\", \"high\", \"high\", \"high\", \"idea\", \"idea\", \"idea\", \"idea\", \"idea\", \"impact\", \"impact\", \"impact\", \"impact\", \"impact\", \"impact\", \"impact\", \"impact\", \"impact\", \"implementation\", \"implementation\", \"implementation\", \"implementation\", \"implementation\", \"implementation\", \"implication\", \"implication\", \"implication\", \"implication\", \"implication\", \"implication\", \"implication\", \"important\", \"important\", \"important\", \"important\", \"important\", \"important\", \"increase\", \"increase\", \"increase\", \"industrial\", \"industrial\", \"industrial\", \"industrial\", \"industry\", \"industry\", \"industry\", \"industry\", \"industry\", \"industry\", \"industry\", \"influence\", \"influence\", \"influence\", \"influence\", \"informa\", \"informa\", \"informa\", \"information\", \"information\", \"information\", \"information\", \"information\", \"information\", \"initial\", \"initial\", \"initial\", \"innovation\", \"innovation\", \"innovation\", \"innovation\", \"innovation\", \"innovation\", \"innovation\", \"innovation\", \"innovative\", \"innovative\", \"innovative\", \"innovative\", \"insight\", \"insight\", \"insight\", \"insight\", \"insight\", \"insight\", \"instead\", \"instead\", \"instead\", \"instead\", \"institution\", \"institution\", \"institution\", \"interest\", \"interest\", \"interest\", \"interest\", \"international\", \"international\", \"international\", \"international\", \"international\", \"internationalisation\", \"internationalisation\", \"internationalisation\", \"internationalisation\", \"introduction\", \"introduction\", \"introduction\", \"investigate\", \"investigate\", \"investigate\", \"investigate\", \"issue\", \"issue\", \"issue\", \"issue\", \"issue\", \"issue\", \"journal\", \"journal\", \"journal\", \"key\", \"key\", \"key\", \"key\", \"key\", \"key\", \"key\", \"key\", \"knowledge\", \"knowledge\", \"knowledge\", \"knowledge\", \"knowledge\", \"knowledge\", \"learning\", \"learning\", \"learning\", \"learning\", \"learning\", \"learning\", \"level\", \"level\", \"level\", \"level\", \"level\", \"level\", \"level\", \"level\", \"licence\", \"licence\", \"licence\", \"light\", \"light\", \"light\", \"limitation\", \"limitation\", \"limited\", \"limited\", \"limited\", \"limited\", \"limited\", \"limited\", \"literature\", \"literature\", \"literature\", \"literature\", \"literature\", \"literature\", \"literature\", \"literature\", \"local\", \"local\", \"local\", \"logic\", \"logic\", \"logic\", \"logic\", \"long\", \"long\", \"loss\", \"loss\", \"loss\", \"loss\", \"low\", \"low\", \"low\", \"low\", \"low\", \"lund\", \"lund\", \"lund\", \"major\", \"major\", \"major\", \"major\", \"management\", \"management\", \"management\", \"management\", \"management\", \"management\", \"manager\", \"manager\", \"manager\", \"manager\", \"manager\", \"manager\", \"manufacturing\", \"manufacturing\", \"manufacturing\", \"market\", \"market\", \"market\", \"market\", \"market\", \"market\", \"market\", \"market\", \"matthew\", \"matthew\", \"measure\", \"measure\", \"measure\", \"measure\", \"measure\", \"mechanism\", \"mechanism\", \"mechanism\", \"medium\", \"medium\", \"medium\", \"medium\", \"member\", \"member\", \"member\", \"member\", \"method\", \"method\", \"method\", \"method\", \"method\", \"methodological\", \"methodological\", \"methodological\", \"model\", \"model\", \"model\", \"model\", \"model\", \"model\", \"model\", \"modelling\", \"modelling\", \"modelling\", \"motivation\", \"motivation\", \"motivation\", \"multi\", \"multi\", \"multi\", \"multinational\", \"multinational\", \"multinational\", \"nature\", \"nature\", \"nature\", \"nature\", \"network\", \"network\", \"network\", \"new\", \"new\", \"new\", \"new\", \"new\", \"new\", \"new\", \"new\", \"non\", \"non\", \"non\", \"non\", \"non\", \"non\", \"non\", \"observation\", \"observation\", \"observation\", \"observation\", \"online\", \"online\", \"online\", \"opportunity\", \"opportunity\", \"opportunity\", \"opportunity\", \"optimization\", \"optimization\", \"order\", \"order\", \"order\", \"order\", \"organisation\", \"organisation\", \"organisation\", \"organization\", \"organization\", \"organization\", \"organization\", \"organizational\", \"organizational\", \"organizational\", \"organizational\", \"organizational\", \"originality\", \"originality\", \"originality\", \"originality\", \"originality\", \"output\", \"output\", \"output\", \"output\", \"output\", \"overall\", \"overall\", \"overall\", \"overall\", \"overall\", \"overall\", \"overview\", \"overview\", \"overview\", \"overview\", \"overview\", \"paper\", \"paper\", \"paper\", \"paper\", \"paper\", \"paper\", \"paper\", \"paper\", \"paper\", \"parameter\", \"parameter\", \"parameter\", \"particular\", \"particular\", \"particular\", \"particular\", \"particular\", \"patent\", \"patent\", \"patent\", \"patent\", \"path\", \"path\", \"path\", \"pattern\", \"pattern\", \"pattern\", \"performance\", \"performance\", \"performance\", \"performance\", \"performance\", \"performance\", \"performance\", \"performance\", \"performance\", \"period\", \"period\", \"period\", \"period\", \"perspective\", \"perspective\", \"perspective\", \"perspective\", \"perspective\", \"perspective\", \"perspective\", \"phenomenon\", \"phenomenon\", \"phenomenon\", \"phenomenon\", \"phenomenon\", \"platform\", \"platform\", \"platform\", \"point\", \"point\", \"point\", \"point\", \"point\", \"policy\", \"policy\", \"policy\", \"policy\", \"policy\", \"policy\", \"policy\", \"policy\", \"positive\", \"positive\", \"positive\", \"positive\", \"positive\", \"positive\", \"positive\", \"positively\", \"positively\", \"positively\", \"potential\", \"potential\", \"potential\", \"potential\", \"potential\", \"potential\", \"potential\", \"power\", \"power\", \"power\", \"power\", \"practical\", \"practical\", \"practical\", \"practice\", \"practice\", \"practice\", \"practice\", \"practice\", \"price\", \"price\", \"price\", \"price\", \"private\", \"private\", \"problem\", \"problem\", \"problem\", \"problem\", \"problem\", \"problem\", \"process\", \"process\", \"process\", \"process\", \"process\", \"process\", \"process\", \"process\", \"product\", \"product\", \"product\", \"product\", \"production\", \"production\", \"production\", \"production\", \"production\", \"production\", \"project\", \"project\", \"project\", \"project\", \"proposition\", \"proposition\", \"proposition\", \"province\", \"province\", \"public\", \"public\", \"public\", \"public\", \"public\", \"publishing\", \"publishing\", \"publishing\", \"publishing\", \"publishing\", \"purpose\", \"purpose\", \"purpose\", \"purpose\", \"purpose\", \"purpose\", \"purpose\", \"qualitative\", \"qualitative\", \"quality\", \"quality\", \"quality\", \"quality\", \"quantitative\", \"quantitative\", \"quantitative\", \"recent\", \"recent\", \"recent\", \"recent\", \"recent\", \"regional\", \"regional\", \"regulation\", \"regulation\", \"regulation\", \"relation\", \"relation\", \"relation\", \"relation\", \"relation\", \"relation\", \"relation\", \"relationship\", \"relationship\", \"relationship\", \"relationship\", \"relationship\", \"relationship\", \"relatively\", \"relatively\", \"relatively\", \"relatively\", \"relevant\", \"relevant\", \"relevant\", \"relevant\", \"relevant\", \"reporting\", \"reporting\", \"reporting\", \"reporting\", \"research\", \"research\", \"research\", \"research\", \"research\", \"research\", \"research\", \"research\", \"research\", \"resource\", \"resource\", \"resource\", \"resource\", \"resource\", \"resource\", \"resource\", \"result\", \"result\", \"result\", \"result\", \"result\", \"result\", \"result\", \"result\", \"result\", \"review\", \"review\", \"review\", \"review\", \"risk\", \"risk\", \"risk\", \"role\", \"role\", \"role\", \"role\", \"role\", \"role\", \"role\", \"sample\", \"sample\", \"sample\", \"sample\", \"sample\", \"scale\", \"scale\", \"scale\", \"scale\", \"scenario\", \"scenario\", \"scholar\", \"scholar\", \"science\", \"science\", \"science\", \"science\", \"second\", \"second\", \"second\", \"second\", \"sector\", \"sector\", \"sector\", \"sector\", \"sector\", \"sector\", \"service\", \"service\", \"service\", \"service\", \"service\", \"significant\", \"significant\", \"significant\", \"significant\", \"significant\", \"significantly\", \"significantly\", \"significantly\", \"significantly\", \"similar\", \"similar\", \"similar\", \"similar\", \"simple\", \"simple\", \"simple\", \"skill\", \"skill\", \"skill\", \"skill\", \"skill\", \"small\", \"small\", \"small\", \"small\", \"small\", \"small\", \"small\", \"sme\", \"sme\", \"sme\", \"social\", \"social\", \"social\", \"social\", \"social\", \"social\", \"social\", \"society\", \"society\", \"society\", \"specific\", \"specific\", \"specific\", \"specific\", \"specific\", \"specifically\", \"specifically\", \"specifically\", \"springer\", \"springer\", \"stage\", \"stage\", \"stage\", \"stage\", \"stakeholder\", \"stakeholder\", \"stakeholder\", \"standard\", \"standard\", \"standard\", \"standard\", \"strategic\", \"strategic\", \"strategic\", \"strategic\", \"strategy\", \"strategy\", \"strategy\", \"strategy\", \"strategy\", \"strategy\", \"strategy\", \"strategy\", \"structure\", \"structure\", \"structure\", \"structure\", \"structure\", \"structure\", \"study\", \"study\", \"study\", \"study\", \"study\", \"study\", \"study\", \"study\", \"study\", \"study\", \"supplier\", \"supplier\", \"supplier\", \"supplier\", \"supply\", \"supply\", \"supply\", \"survey\", \"survey\", \"survey\", \"survey\", \"survey\", \"sustainability\", \"sustainability\", \"sustainability\", \"sustainability\", \"sustainability\", \"sustainability\", \"sustainable\", \"sustainable\", \"sustainable\", \"sustainable\", \"sustainable\", \"sustainable\", \"switzerland\", \"switzerland\", \"switzerland\", \"switzerland\", \"system\", \"system\", \"system\", \"system\", \"system\", \"system\", \"system\", \"system\", \"systematic\", \"systematic\", \"systematic\", \"taylor\", \"taylor\", \"taylor\", \"taylor\", \"taylor\", \"technique\", \"technique\", \"technological\", \"technological\", \"technological\", \"technological\", \"technological\", \"technology\", \"technology\", \"technology\", \"technology\", \"technology\", \"term\", \"term\", \"term\", \"term\", \"theoretical\", \"theoretical\", \"theoretical\", \"theoretical\", \"theoretically\", \"theoretically\", \"theoretically\", \"theoretically\", \"theory\", \"theory\", \"theory\", \"theory\", \"time\", \"time\", \"time\", \"time\", \"time\", \"time\", \"time\", \"topic\", \"topic\", \"topic\", \"trading\", \"trading\", \"trading\", \"trading\", \"transition\", \"transition\", \"transition\", \"turn\", \"turn\", \"turn\", \"uk\", \"uk\", \"uk\", \"uk\", \"uncertainty\", \"uncertainty\", \"uncertainty\", \"uncertainty\", \"understanding\", \"understanding\", \"understanding\", \"unique\", \"unique\", \"unique\", \"university\", \"university\", \"use\", \"use\", \"use\", \"use\", \"user\", \"user\", \"user\", \"value\", \"value\", \"value\", \"value\", \"value\", \"value\", \"value\", \"value\", \"value\", \"venture\", \"venture\", \"venture\", \"venture\", \"wide\", \"wide\", \"wide\", \"work\", \"work\", \"work\", \"work\", \"work\", \"world\", \"world\", \"world\", \"world\", \"world\", \"world\", \"year\", \"year\", \"year\", \"year\", \"year\"]}, \"R\": 30, \"lambda.step\": 0.01, \"plot.opts\": {\"xlab\": \"PC1\", \"ylab\": \"PC2\"}, \"topic.order\": [7, 6, 3, 5, 10, 4, 2, 1, 8, 9]};\n",
              "\n",
              "function LDAvis_load_lib(url, callback){\n",
              "  var s = document.createElement('script');\n",
              "  s.src = url;\n",
              "  s.async = true;\n",
              "  s.onreadystatechange = s.onload = callback;\n",
              "  s.onerror = function(){console.warn(\"failed to load library \" + url);};\n",
              "  document.getElementsByTagName(\"head\")[0].appendChild(s);\n",
              "}\n",
              "\n",
              "if(typeof(LDAvis) !== \"undefined\"){\n",
              "   // already loaded: just create the visualization\n",
              "   !function(LDAvis){\n",
              "       new LDAvis(\"#\" + \"ldavis_el721396825743015204915803559\", ldavis_el721396825743015204915803559_data);\n",
              "   }(LDAvis);\n",
              "}else if(typeof define === \"function\" && define.amd){\n",
              "   // require.js is available: use it to load d3/LDAvis\n",
              "   require.config({paths: {d3: \"https://d3js.org/d3.v5\"}});\n",
              "   require([\"d3\"], function(d3){\n",
              "      window.d3 = d3;\n",
              "      LDAvis_load_lib(\"https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.3.1/pyLDAvis/js/ldavis.v3.0.0.js\", function(){\n",
              "        new LDAvis(\"#\" + \"ldavis_el721396825743015204915803559\", ldavis_el721396825743015204915803559_data);\n",
              "      });\n",
              "    });\n",
              "}else{\n",
              "    // require.js not available: dynamically load d3 & LDAvis\n",
              "    LDAvis_load_lib(\"https://d3js.org/d3.v5.js\", function(){\n",
              "         LDAvis_load_lib(\"https://cdn.jsdelivr.net/gh/bmabey/pyLDAvis@3.3.1/pyLDAvis/js/ldavis.v3.0.0.js\", function(){\n",
              "                 new LDAvis(\"#\" + \"ldavis_el721396825743015204915803559\", ldavis_el721396825743015204915803559_data);\n",
              "            })\n",
              "         });\n",
              "}\n",
              "</script>"
            ]
          },
          "metadata": {},
          "execution_count": 18
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Calculating the coherence score for 10 topics (defined in lda_model)"
      ],
      "metadata": {
        "id": "jLJ18hw_AM0f"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# imports\n",
        "from gensim.models import CoherenceModel"
      ],
      "metadata": {
        "id": "f742buiD1ZqK"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Computing the Coherence Score\n",
        "\n",
        "cm = CoherenceModel(model=lda_model, texts=data['tokens'], dictionary=dictionary, coherence='u_mass')\n",
        "coherence = cm.get_coherence()\n",
        "print('\\nCoherence Score: ', coherence)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "_-07puNY16sp",
        "outputId": "76ca3259-a960-4eef-be47-54700b37f012"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Coherence Score:  -4.308610280842419\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "RJ add-on calculations/solutions (not performed by NHN)"
      ],
      "metadata": {
        "id": "G_yVPBdiA5WU"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "cm = CoherenceModel(model=lda_model, corpus=corpus, coherence='u_mass')\n",
        "coherence = cm.get_coherence()  # get coherence value"
      ],
      "metadata": {
        "id": "pBzQmhs_WNSq"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "data = data.reset_index()"
      ],
      "metadata": {
        "id": "Ul1vX_Q-eW6G"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "data.shape"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "51DHdta-Qc6x",
        "outputId": "bac06939-c377-4cc8-c149-08a85fa9ca14"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "(135, 10)"
            ]
          },
          "metadata": {},
          "execution_count": 23
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "data = data[data[\"tokens\"].str.len() != 0]"
      ],
      "metadata": {
        "id": "FnuDSiYzQV6f"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "data"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 1000
        },
        "id": "WrPGMwXOeseM",
        "outputId": "75483c8f-8122-40e1-ff90-598090e27d5f"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "     index                                            Authors  \\\n",
              "0        0                    Gao Y., Hu Y., Liu X., Zhang H.   \n",
              "1        1  Xu X., Hu W., Liu W., Wang D., Huang Q., Huang...   \n",
              "2        2   Xu X., Hu W., Liu W., Wang D., Huang Q., Chen Z.   \n",
              "3        3           Saabye H., Kristensen T.B., Wæhrens B.V.   \n",
              "4        4             Crovini C., Ossola G., Britzelmaier B.   \n",
              "..     ...                                                ...   \n",
              "130    130  Bhatti W.A., Chwialkowska A., Nickell D., Roll...   \n",
              "131    131  Joseph K.J., Cozzens S., De Fuentes C., Dutrén...   \n",
              "132    132                        Madsen K.M., Rasmussen M.H.   \n",
              "133    133                           Larsen M.V., Madsen C.Ø.   \n",
              "134    134                             Hertel F., Wicmandy M.   \n",
              "\n",
              "                                          Author(s) ID  \\\n",
              "0     57196280682;56580618100;35208483000;57169423400;   \n",
              "1    57205534107;24921323300;57193691954;5676303010...   \n",
              "2    57205534107;24921323300;57193691954;5676303010...   \n",
              "3                 57219656715;57213084303;22837185500;   \n",
              "4                  57200919718;6602427174;23471680600;   \n",
              "..                                                 ...   \n",
              "130   55929356400;57205719975;53264695100;36722255000;   \n",
              "131  55601591500;6602428817;57202908940;55989644900...   \n",
              "132                           57209279493;57223096079;   \n",
              "133                           57162157200;57162540600;   \n",
              "134                           57207916203;57222105086;   \n",
              "\n",
              "                                                 Title  \\\n",
              "0    Can Public R&D Subsidy Facilitate Firms’ Explo...   \n",
              "1    Risk-based scheduling of an off-grid hybrid el...   \n",
              "2    Study on the economic benefits of retired elec...   \n",
              "3    Real-time data utilization barriers to improvi...   \n",
              "4    How to reconsider risk management in SMEs? An ...   \n",
              "..                                                 ...   \n",
              "130  Market knowledge learning in emerging markets:...   \n",
              "131             A decade of innovation and development   \n",
              "132       A Matrix for Gamifying Development Workshops   \n",
              "133  Co-production as seen from a top management pe...   \n",
              "134  Metaphorical creativity: an aspect of everyday...   \n",
              "\n",
              "                                              Abstract  Year  \\\n",
              "0    Public R&D subsidy is a commonly adopted polic...  2021   \n",
              "1    Making full use of renewable energy to supply ...  2021   \n",
              "2    The lithium-ion batteries of battery electric ...  2021   \n",
              "3    This study presents empirical evidence for the...  2020   \n",
              "4    The purpose of this paper is two-fold: to reco...  2021   \n",
              "..                                                 ...   ...   \n",
              "130  The turbulent environment that occurs within e...  2021   \n",
              "131  This year marks the tenth anniversary of Innov...  2021   \n",
              "132  The interest in potentials of gamification for...  2021   \n",
              "133  This chapter addresses the 'co-production turn...  2020   \n",
              "134  Purpose: According to Mumford et al. (2018), c...  2020   \n",
              "\n",
              "                                          Source title  \\\n",
              "0                                      Research Policy   \n",
              "1                        Journal of Cleaner Production   \n",
              "2                        Journal of Cleaner Production   \n",
              "3                         Sustainability (Switzerland)   \n",
              "4                          European Management Journal   \n",
              "..                                                 ...   \n",
              "130  International Journal of Management and Decisi...   \n",
              "131                         Innovation and Development   \n",
              "132  Lecture Notes of the Institute for Computer Sc...   \n",
              "133  Processual Perspectives on the Co-Production T...   \n",
              "134          Development and Learning in Organizations   \n",
              "\n",
              "                                                  text  \\\n",
              "0    Can Public R&D Subsidy Facilitate Firms’ Explo...   \n",
              "1    Risk-based scheduling of an off-grid hybrid el...   \n",
              "2    Study on the economic benefits of retired elec...   \n",
              "3    Real-time data utilization barriers to improvi...   \n",
              "4    How to reconsider risk management in SMEs? An ...   \n",
              "..                                                 ...   \n",
              "130  Market knowledge learning in emerging markets:...   \n",
              "131  A decade of innovation and development. This y...   \n",
              "132  A Matrix for Gamifying Development Workshops. ...   \n",
              "133  Co-production as seen from a top management pe...   \n",
              "134  Metaphorical creativity: an aspect of everyday...   \n",
              "\n",
              "                                            text_clean  \\\n",
              "0    public subsidy facilitate firms exploratory in...   \n",
              "1    risk based scheduling grid hybrid electricity ...   \n",
              "2    study economic benefits retired electric vehic...   \n",
              "3    real time data utilization barriers improving ...   \n",
              "4    reconsider risk management smes advanced reaso...   \n",
              "..                                                 ...   \n",
              "130  market knowledge learning emerging markets emp...   \n",
              "131  decade innovation development year marks tenth...   \n",
              "132  matrix gamifying development workshops interes...   \n",
              "133  co production seen management perspective chap...   \n",
              "134  metaphorical creativity aspect everyday creati...   \n",
              "\n",
              "                                                tokens  \n",
              "0    [public, subsidy, facilitate, firm, explorator...  \n",
              "1    [risk, scheduling, grid, hybrid, electricity, ...  \n",
              "2    [economic, benefit, electric, vehicle, battery...  \n",
              "3    [real, time, data, utilization, barrier, produ...  \n",
              "4    [risk, management, sme, advanced, literature, ...  \n",
              "..                                                 ...  \n",
              "130  [market, knowledge, market, empirical, study, ...  \n",
              "131  [decade, innovation, development, year, tenth,...  \n",
              "132  [matrix, gamifying, development, workshop, int...  \n",
              "133  [co, production, management, perspective, chap...  \n",
              "134  [metaphorical, creativity, aspect, everyday, c...  \n",
              "\n",
              "[135 rows x 10 columns]"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-f4583e2d-35d7-4ff2-9c9b-017f8cfd74f9\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>index</th>\n",
              "      <th>Authors</th>\n",
              "      <th>Author(s) ID</th>\n",
              "      <th>Title</th>\n",
              "      <th>Abstract</th>\n",
              "      <th>Year</th>\n",
              "      <th>Source title</th>\n",
              "      <th>text</th>\n",
              "      <th>text_clean</th>\n",
              "      <th>tokens</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>0</td>\n",
              "      <td>Gao Y., Hu Y., Liu X., Zhang H.</td>\n",
              "      <td>57196280682;56580618100;35208483000;57169423400;</td>\n",
              "      <td>Can Public R&amp;D Subsidy Facilitate Firms’ Explo...</td>\n",
              "      <td>Public R&amp;D subsidy is a commonly adopted polic...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Research Policy</td>\n",
              "      <td>Can Public R&amp;D Subsidy Facilitate Firms’ Explo...</td>\n",
              "      <td>public subsidy facilitate firms exploratory in...</td>\n",
              "      <td>[public, subsidy, facilitate, firm, explorator...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>1</td>\n",
              "      <td>Xu X., Hu W., Liu W., Wang D., Huang Q., Huang...</td>\n",
              "      <td>57205534107;24921323300;57193691954;5676303010...</td>\n",
              "      <td>Risk-based scheduling of an off-grid hybrid el...</td>\n",
              "      <td>Making full use of renewable energy to supply ...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Journal of Cleaner Production</td>\n",
              "      <td>Risk-based scheduling of an off-grid hybrid el...</td>\n",
              "      <td>risk based scheduling grid hybrid electricity ...</td>\n",
              "      <td>[risk, scheduling, grid, hybrid, electricity, ...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>2</td>\n",
              "      <td>Xu X., Hu W., Liu W., Wang D., Huang Q., Chen Z.</td>\n",
              "      <td>57205534107;24921323300;57193691954;5676303010...</td>\n",
              "      <td>Study on the economic benefits of retired elec...</td>\n",
              "      <td>The lithium-ion batteries of battery electric ...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Journal of Cleaner Production</td>\n",
              "      <td>Study on the economic benefits of retired elec...</td>\n",
              "      <td>study economic benefits retired electric vehic...</td>\n",
              "      <td>[economic, benefit, electric, vehicle, battery...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>3</td>\n",
              "      <td>Saabye H., Kristensen T.B., Wæhrens B.V.</td>\n",
              "      <td>57219656715;57213084303;22837185500;</td>\n",
              "      <td>Real-time data utilization barriers to improvi...</td>\n",
              "      <td>This study presents empirical evidence for the...</td>\n",
              "      <td>2020</td>\n",
              "      <td>Sustainability (Switzerland)</td>\n",
              "      <td>Real-time data utilization barriers to improvi...</td>\n",
              "      <td>real time data utilization barriers improving ...</td>\n",
              "      <td>[real, time, data, utilization, barrier, produ...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>4</td>\n",
              "      <td>Crovini C., Ossola G., Britzelmaier B.</td>\n",
              "      <td>57200919718;6602427174;23471680600;</td>\n",
              "      <td>How to reconsider risk management in SMEs? An ...</td>\n",
              "      <td>The purpose of this paper is two-fold: to reco...</td>\n",
              "      <td>2021</td>\n",
              "      <td>European Management Journal</td>\n",
              "      <td>How to reconsider risk management in SMEs? An ...</td>\n",
              "      <td>reconsider risk management smes advanced reaso...</td>\n",
              "      <td>[risk, management, sme, advanced, literature, ...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>...</th>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "      <td>...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>130</th>\n",
              "      <td>130</td>\n",
              "      <td>Bhatti W.A., Chwialkowska A., Nickell D., Roll...</td>\n",
              "      <td>55929356400;57205719975;53264695100;36722255000;</td>\n",
              "      <td>Market knowledge learning in emerging markets:...</td>\n",
              "      <td>The turbulent environment that occurs within e...</td>\n",
              "      <td>2021</td>\n",
              "      <td>International Journal of Management and Decisi...</td>\n",
              "      <td>Market knowledge learning in emerging markets:...</td>\n",
              "      <td>market knowledge learning emerging markets emp...</td>\n",
              "      <td>[market, knowledge, market, empirical, study, ...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>131</th>\n",
              "      <td>131</td>\n",
              "      <td>Joseph K.J., Cozzens S., De Fuentes C., Dutrén...</td>\n",
              "      <td>55601591500;6602428817;57202908940;55989644900...</td>\n",
              "      <td>A decade of innovation and development</td>\n",
              "      <td>This year marks the tenth anniversary of Innov...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Innovation and Development</td>\n",
              "      <td>A decade of innovation and development. This y...</td>\n",
              "      <td>decade innovation development year marks tenth...</td>\n",
              "      <td>[decade, innovation, development, year, tenth,...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>132</th>\n",
              "      <td>132</td>\n",
              "      <td>Madsen K.M., Rasmussen M.H.</td>\n",
              "      <td>57209279493;57223096079;</td>\n",
              "      <td>A Matrix for Gamifying Development Workshops</td>\n",
              "      <td>The interest in potentials of gamification for...</td>\n",
              "      <td>2021</td>\n",
              "      <td>Lecture Notes of the Institute for Computer Sc...</td>\n",
              "      <td>A Matrix for Gamifying Development Workshops. ...</td>\n",
              "      <td>matrix gamifying development workshops interes...</td>\n",
              "      <td>[matrix, gamifying, development, workshop, int...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>133</th>\n",
              "      <td>133</td>\n",
              "      <td>Larsen M.V., Madsen C.Ø.</td>\n",
              "      <td>57162157200;57162540600;</td>\n",
              "      <td>Co-production as seen from a top management pe...</td>\n",
              "      <td>This chapter addresses the 'co-production turn...</td>\n",
              "      <td>2020</td>\n",
              "      <td>Processual Perspectives on the Co-Production T...</td>\n",
              "      <td>Co-production as seen from a top management pe...</td>\n",
              "      <td>co production seen management perspective chap...</td>\n",
              "      <td>[co, production, management, perspective, chap...</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>134</th>\n",
              "      <td>134</td>\n",
              "      <td>Hertel F., Wicmandy M.</td>\n",
              "      <td>57207916203;57222105086;</td>\n",
              "      <td>Metaphorical creativity: an aspect of everyday...</td>\n",
              "      <td>Purpose: According to Mumford et al. (2018), c...</td>\n",
              "      <td>2020</td>\n",
              "      <td>Development and Learning in Organizations</td>\n",
              "      <td>Metaphorical creativity: an aspect of everyday...</td>\n",
              "      <td>metaphorical creativity aspect everyday creati...</td>\n",
              "      <td>[metaphorical, creativity, aspect, everyday, c...</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>135 rows × 10 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-f4583e2d-35d7-4ff2-9c9b-017f8cfd74f9')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-f4583e2d-35d7-4ff2-9c9b-017f8cfd74f9 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-f4583e2d-35d7-4ff2-9c9b-017f8cfd74f9');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 25
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import seaborn as sns\n",
        "import matplotlib.pyplot as plt\n",
        "import numpy as np\n",
        "from gensim.models import LdaModel, CoherenceModel\n",
        "from gensim import corpora"
      ],
      "metadata": {
        "id": "gB_lko8FsN8Q"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "corpus = data['tokens']"
      ],
      "metadata": {
        "id": "YC4LGwpOsXCD"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "corpus"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "a4hWPw6xxW6o",
        "outputId": "371eb446-26f2-4c3b-8b7c-e362546e34a3"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "0      [public, subsidy, facilitate, firm, explorator...\n",
              "1      [risk, scheduling, grid, hybrid, electricity, ...\n",
              "2      [economic, benefit, electric, vehicle, battery...\n",
              "3      [real, time, data, utilization, barrier, produ...\n",
              "4      [risk, management, sme, advanced, literature, ...\n",
              "                             ...                        \n",
              "130    [market, knowledge, market, empirical, study, ...\n",
              "131    [decade, innovation, development, year, tenth,...\n",
              "132    [matrix, gamifying, development, workshop, int...\n",
              "133    [co, production, management, perspective, chap...\n",
              "134    [metaphorical, creativity, aspect, everyday, c...\n",
              "Name: tokens, Length: 135, dtype: object"
            ]
          },
          "metadata": {},
          "execution_count": 28
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "dirichlet_dict = corpora.Dictionary(corpus)\n",
        "bow_corpus = [dirichlet_dict.doc2bow(text) for text in corpus]\n",
        "\n",
        "# Considering 1-15 topics, as the last is cut off\n",
        "num_topics = list(range(16)[1:])\n",
        "num_keywords = 15\n",
        "\n",
        "LDA_models = {}\n",
        "LDA_topics = {}\n",
        "for i in num_topics:\n",
        "    LDA_models[i] = LdaModel(corpus=bow_corpus,\n",
        "                             id2word=dirichlet_dict,\n",
        "                             num_topics=i,\n",
        "                             update_every=1,\n",
        "                             chunksize=len(bow_corpus),\n",
        "                             passes=20,\n",
        "                             alpha='auto',\n",
        "                             random_state=42)\n",
        "\n",
        "    shown_topics = LDA_models[i].show_topics(num_topics=i, \n",
        "                                             num_words=num_keywords,\n",
        "                                             formatted=False)\n",
        "    LDA_topics[i] = [[word[0] for word in topic[1]] for topic in shown_topics]"
      ],
      "metadata": {
        "id": "g6M0SE0nr7KO"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def jaccard_similarity(topic_1, topic_2):\n",
        "    \"\"\"\n",
        "    Derives the Jaccard similarity of two topics\n",
        "\n",
        "    Jaccard similarity:\n",
        "    - A statistic used for comparing the similarity and diversity of sample sets\n",
        "    - J(A,B) = (A ∩ B)/(A ∪ B)\n",
        "    - Goal is low Jaccard scores for coverage of the diverse elements\n",
        "    \"\"\"\n",
        "    intersection = set(topic_1).intersection(set(topic_2))\n",
        "    union = set(topic_1).union(set(topic_2))\n",
        "                    \n",
        "    return float(len(intersection))/float(len(union))"
      ],
      "metadata": {
        "id": "ZzK6Q8B1s5gd"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "LDA_stability = {}\n",
        "for i in range(0, len(num_topics)-1):\n",
        "    jaccard_sims = []\n",
        "    for t1, topic1 in enumerate(LDA_topics[num_topics[i]]): # pylint: disable=unused-variable\n",
        "        sims = []\n",
        "        for t2, topic2 in enumerate(LDA_topics[num_topics[i+1]]): # pylint: disable=unused-variable\n",
        "            sims.append(jaccard_similarity(topic1, topic2))    \n",
        "        \n",
        "        jaccard_sims.append(sims)    \n",
        "    \n",
        "    LDA_stability[num_topics[i]] = jaccard_sims\n",
        "                \n",
        "mean_stabilities = [np.array(LDA_stability[i]).mean() for i in num_topics[:-1]]"
      ],
      "metadata": {
        "id": "8CqBHt5ewRjf"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "coherences = [CoherenceModel(model=LDA_models[i], texts=corpus, dictionary=dirichlet_dict, coherence='c_v').get_coherence() for i in num_topics[:-1]]"
      ],
      "metadata": {
        "id": "LxgSm8mbwWSP"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "coh_sta_diffs = [coherences[i] - mean_stabilities[i] for i in range(num_keywords)[:-1]] # limit topic numbers to the number of keywords\n",
        "coh_sta_max = max(coh_sta_diffs)\n",
        "coh_sta_max_idxs = [i for i, j in enumerate(coh_sta_diffs) if j == coh_sta_max]\n",
        "ideal_topic_num_index = coh_sta_max_idxs[0] # choose less topics in case there's more than one max\n",
        "ideal_topic_num = num_topics[ideal_topic_num_index]"
      ],
      "metadata": {
        "id": "FgQ7NBBOwzru"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "plt.figure(figsize=(20,10))\n",
        "ax = sns.lineplot(x=num_topics[:-1], y=mean_stabilities, label='Average Topic Overlap')\n",
        "ax = sns.lineplot(x=num_topics[:-1], y=coherences, label='Topic Coherence')\n",
        "\n",
        "ax.axvline(x=ideal_topic_num, label='Ideal Number of Topics', color='black')\n",
        "ax.axvspan(xmin=ideal_topic_num - 1, xmax=ideal_topic_num + 1, alpha=0.5, facecolor='grey')\n",
        "\n",
        "y_max = max(max(mean_stabilities), max(coherences)) + (0.10 * max(max(mean_stabilities), max(coherences)))\n",
        "ax.set_ylim([0, y_max])\n",
        "ax.set_xlim([1, num_topics[-1]-1])\n",
        "                \n",
        "ax.axes.set_title('Model Metrics per Number of Topics', fontsize=25)\n",
        "ax.set_ylabel('Metric Level', fontsize=20)\n",
        "ax.set_xlabel('Number of Topics', fontsize=20)\n",
        "plt.legend(fontsize=20)\n",
        "plt.show()  "
      ],
      "metadata": {
        "id": "69zOLWwGwb_7",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 639
        },
        "outputId": "247c222d-2d78-442e-df4c-765b386eac6a"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 1440x720 with 1 Axes>"
            ],
            "image/png": "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938MHz6cVq1aUahQxt1C0tLSePfdd0lPT6d79+42zx04cCDr1683bzAeHx/P8OHDAejWrVuO1y1UqBAvv/wyc+bM4d133832rna3m6ETEhJCp06dmDVrFi1btmTx4sUUL17cos/kyZMZNWoU7u7uVrPSAFxcXHjppZeYNm0aX331FdHR0bRq1crqc1G4cGE6duzIrFmz+OSTTxg0aJDVjK/Dhw9jNBpt7rN0JwIDAzl48CCnTp0yLw00mUwMHTqUPXv2ZHteWloa77//PnPnzjW/njExMYwfPx57e3v++9///qO6REREROTuuTjaUaqQO6VymDV14XLyLTOmrpnv0PdXLmZNZdydz3JJn5erZk3Jo0nB0yNs06ZNHDhwgCeeeCLHTZe7d+/Op59+SlhYGMOGDTPfXaxLly6sW7eOQYMGmR/bMmfOHBo3bkz37t0ZP348tWvXxsvLixMnTvDHH3+we/duIiMjcx08de7cmS+++IK+ffuyceNGypYty8GDB1mxYgVt2rRh3rx5VudMnDiR+vXr89Zbb7Fy5UoqV67MkSNHWLRoES+88AJLly61CFwcHBz48ccfadasGS1atKBevXpUqVIFV1dXjh8/TlRUFEeOHOH06dP3JHiqV68e/fv35/PPP6dSpUq0a9cONzc3Vq1axe7duwkODua9996zOq9o0aJcv36dSpUq0apVK1JSUli4cCGnT5/mrbfeIiQk5LbXnjBhArt372by5Mls2rSJZs2a4ejoSExMDOHh4Sxbtsy8WXlOpk6dSmpqKnPnziUoKIhnn32WsmXLcvnyZTZu3Mju3bspWLAgixYtomLFijbH6NKlC9OmTWPgwIHmx9nVfPDgQT766CNmzZpFcHAwfn5+nDp1ir179xIVFcXcuXP/cfD0zjvv0KNHD6pWrUrbtm1xcHDg559/Zs+ePTz//PMsX77c5nmVK1fm119/pXr16jRt2pTExETmz59PYmIin3/+uc3llCIiIiJyfzAaDRTycKKQhxNPZjNr6lpKmnn5nsVyvqSr7Dl1kbV7zpKcmrtZU0U9nfF2c8TL1QFvV0ecHaz3cBV5kCl4eoRlznZ69dVXc+wXGBhIkyZNWLt2LcuXL6d169ZAxtKot99+m4sXL1KpUiWqVatm8/zixYvz+++/8/XXX7No0SK+//570tLSKFKkCBUrVqRXr14W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MmrUKKpWrcqECROYOXMmKSkplC5dmuHDh9OvXz+bG3A7Ojqybt06Bg0axA8//EBcXBylSpViwIAB9OrVK1fX9fb2Ztu2bYwdO5Z58+YxdepU7OzsCAgIIDQ01OrObNlxcHDgm2++oWvXrkydOpWtW7fyyy+/kJKSQuHChalRowZjxoyxCJ4A5s6dS4MGDfjuu++YMmUKABUqVKBfv368+eabubr27bz//vvUr1+f8ePHExERwdKlS/H09MTf35/XX3+dDh063NF4Tz/9NH/88QejR48mPDycrVu34ujoSLFixWjcuDFt27b9xzXXqFGDXbt2MXLkSFatWsW2bdvw8PCgTJkyfPzxxxZ9K1euTHR0NF9++SUrVqwgLCwMo9FI0aJFqVq1KsOGDcPX1/cf1yQiIiIiIiL3H4PJZMrvGu65GjVqmH777bfb9tu7dy8VKlT4Fyp69AQGBgIQGxubr3WIPEz0PUtE5OH0T5fBi7W+ffsCMHbs2Hyu5OGTm9UGIvLwMhgMv5tMphp3co72eBIRERERERERkTyh4ElERERERERERPKEgicREREREREREckT2lxc8oT2dhIRERERERERzXgSEREREREREZE8oeBJRERERERERETyhIInERERERERERHJEwqeREREREREREQkTyh4EhERERERERGRPKHgSURERERERERE8oSCJxERERERERERyRMKnkREREREREREJE8oeBIRERERERERkTyh4EnuSmBgIIGBgf/6dbt27YrBYCA2NvZfv/a/bfr06RgMBqZPn57fpdwzKSkpDBkyhLJly+Lk5ITBYGDJkiX5XVauNGzYEIPBkN9liIiIiIiIPFAUPAkGg+Gh/YE6M6gyGAysXLnSZp+hQ4diMBiYNm3av1zdo2fMmDF8/PHHFCtWjHfffZchQ4ZQvnx5m32zvne5+dOwYcN/98mIiIiIiIjIbdnndwEi/5b+/fvTrFkz7Ozs8ruUR9aKFStwd3dn7dq1ODo65tj3xRdftJpVt2nTJjZv3kyDBg2sgqa8noE3c+ZMrly5kqfXEBERERERedgoeJJHQpkyZfjrr7/47rvveO211/K7nEfWqVOnKFiw4G1DJ8gInl588UWLtqFDh7J582YaNmzI0KFD86hK20qUKPGvXk9ERERERORhoKV2ki2TycSECRN4/PHHcXZ2xt/f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\n"
          },
          "metadata": {
            "needs_background": "light"
          }
        }
      ]
    }
  ]
}
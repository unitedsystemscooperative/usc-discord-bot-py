from quickchart import QuickChart


class Charts():
    @staticmethod
    def generate_vote_chart(*, labels: list[str] = None, data: list[int] = None) -> str:
        if labels is None:
            raise ValueError('Labels is blank')
        if data is None:
            raise ValueError('data is blank')

        chart = QuickChart()
        chart.width = 500
        chart.height = 300
        chart.config = f"""{{
            type: 'bar',
            data: {{
              labels: {labels},
              datasets: [
                {{
                  label: 'Votes',
                  backgroundColor: 'rgba(255, 99, 132, 0.5)',
                  borderColor: 'rgb(255, 99, 132)',
                  borderWidth: 1,
                  data: {data},
                }}
              ],
            }},
            options: {{
              title: {{
                display: true,
                text: 'Bar Chart',
              }},
              plugins: {{
                datalabels: {{
                  anchor: 'center',
                  align: 'center',
                  color: '#666',
                  font: {{
                    weight: 'normal',
                  }},
                }},
              }},
            }},
        }}"""

        return chart.get_url()

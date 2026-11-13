# Dashboard Desing

> In this .md file i lay down the process through which i created the dashboard.

## My 6-phase workflow

### Phase 1. Purpose and audience - "The why?"

It is important to define the main objective of the dashboard before even start thinking about its specifics. Since dahsboards are used to facilitate optimal decision making, we need to think which is the single most important decision that the end-user needs to make using said dashboard.

Said question is none other than "Where should i allocate my money and what can i expect from said portfolio?". The overall purpose of the project is to give the user the single best asset allocation combination based on certain specific criteria. Thus, the whole dahsboard should be focused on giving relevant information about said best portfolio, as well as how it compares to other porfolios (for we need to know how something compares to other things to clearly identify why it is indeed the best option).

### Phase 2. Data architectura and modeling - The "fundation"

Here we need to clearly define the overall structure of the underlying data model. We need to properly define how are relationships between tables defined, or how will we create said relationships using DAX measures or power pivot transformations.

This part is simple, for we only have two tables, and both are connected by the same key "Portfolio_ID". In the markowitz model associated table, said key is its primary key. On the 2nd table, said key, along the "Path" key form a compound primary key. It wont be necessary to tie both tables using DAX measures or data transformations, for the connection was already established in the data processing done in python.

Now, there are two isues that need to be tackled. First, the markowitz_model table needs to suffer a data transformation in order to be able to properly create the treemap that will display the weight allocation for each asset. Treemaps require a single column for the "Category" data field, and by default the table has the weights unpivoted. This needs to be changed. Secondly, notice that the gbm stress test table list each of the three Portfolio_IDs thousands of times. This must not be an impediment, but it is necessary to consider it.

### Phase 3. The narrative hierachy - The "Wireframe"

In this phase we structure the dashboard using the standard Business Intelligence "Overview to Detail" approach. The layout looks like this:

- Top (The Executive Summary): High-level KPI cards that display single, crucial numbers which update instantly based on user selection.
- Middle (The Hero Visuals): The core interactive charts that drive the story and allow cross-filtering (e.g., the efficient frontier scatter plot and the asset allocation tree map).
- Bottom (The Granular Detail): Time-series analysis showing progression over time (e.g., the GBM stress test line chart).
- Margins (Navigation & Filtering): Slicer buttons to easily switch between your identified optimal targets, such as "Max Sharpe", "Min Variance", and "Max Return".

Before tackling each, we first list all relevant data and information that may be worth including in some part of the dashboard. We identify the following broad categories of information:

1. Pertaining selected portfolios.
2. Pertaining selected optimal porfolios.
3. Pertaining the overall sample of portfolios.

Now we detail possible interesting info to cover for each:

#### Info Pertaining selected portfolios

By selected portfolios we mean the current active porfolio which is not an optimal one, chosen by clicking on the scatter diagram one of the many points. For these portfolios, we wont show information related to the 2026 projection, for there is none. But there are still useful metrics that can be displayed, like:

- Value of the Sharpe Ratio
- Expected yearly return
- Risk of the portfolio
- Weight distribution of the portfolio

Also, some maybes are:

- Percentile position for each metric (like a subtitle in the kpi cards associated to the above mentioned metrics, stating that this porfolio is in the 50th percentile and such).
- Special coloring for specific groups of values.
- 

#### Info Pertaining selected optimal porfolios

When choosing one of the three best portfolios, extra information must be shown, for we have the 500 YTD projection data. Now, somehow we must solve the issue of showing this extra info only when these porfolios are chosen. This poses a problem, for if we use a single page for the dahsboard, we need to handle the uncomfortable case of displaying extra info when these specific porfolios are chosen. This problem will be tackled later.

Regarding the metrics or info to be displayed we have:

- Fan chart that summarizes the 500 paths
    - It would be nice to desing the fan chart so it displays precentile grouping areas. Like, the paths that the 10th to 90th percentile of paths take, the paths that the lower 10th percentiles take, and the same for the 90th to 100th.


#### Info Pertaining the overall sample of porfolios

This are a maybe. The end-user may not be interested in the whole picture, just in the best porfolios, and even less in some kind of summary metrics of the whole 5000 portfolios. Still, i will include some ideas:

- The number of computed portfolios.
- The maximum and minimum of (sharp ratio, maximum return, risk)

#### Amount of pages

Going back to the issue of only having the gbm simulations for the chosen optimal porfolios, it becomes necessary to have two pages for the dashboard. Hiding the scatter plot when an optimal porfolio is chosen and showing the fan-like chart is not ideal, for then the user loses the capacity of comparing portfolios and comparing the **oportunity cost** that said portfolios suppose. Not without mentioning the user experience issues where they wont be able to easily select another porfolio, for the scatter plot was hiden.

To solve this there are two available options: **(1)** Use the "Bookmarks and Selection Pane" to make the fan chart to appear in a new overlaying window when an optimal porfolio is chosen; and **(2)** to just create a new page. The 2nd option is the most logical one, for it does make sense to isolate each part of the simulation (the markowitz model and the gbm projection) in different pages, after all, they consitute separate analysis that serve different purposes.

#### Page 1: The markowitz model

Here i lay out the contents of each of the parts of the "Overwiew to detail" approach to the 1st page; the page associated to the markowtiz model.

##### The Top - "Executive Summary"

This will be placed in a rectangle at the top of the page, spanning from the left border to the right border. Three main KPI's will be placed here: **(1)** The expected yearly return; **(2)** The yearly risk, and **(3)** the value of the sharpe ratio. All of the currently selected portfolio. By default the max sharpe porfiolio will be selected.

Now, in these KPI boxes more info will be displayed. For now the candidates for the info to be display in grey subtitles, with a lower font size, are:

- yearly expected return
    - In which percentile does the return fall?
    - Is this the best porfolio with this return level? i.e., are there porfolios with the same or more return percentage that have less risk?
    - Is this bellow the efficient frontier?
- yearly risk
    - In which percentile does the return fall?
    - Is this the best portfolio for this risk level?
    - Is this bellow the efficient frontier?
- Sharpe ratio
    - In which percentile does the value fall?
    - How far from the best sharpe ratio is its value?
    - Is this below the efficient frontier?

Now, i will critique my own ideas: It makes no sense to show in each and not even in a single one kpi card if the selected portfolio is below the efficient frontier. All the information inside those kpi boxes should be relevant to the kpi itself, not to the portfolio as a whole. Also, to actually get some useful information when reading "below the efficient fontier" one would need to look at the scatter plot, which does not seem right (for we dont want to be playing with the users attention).

Now, for the questions "is this the best porfolio for this risk level"? A simple, "yer" or "no" answer does not suffice. We would need to show how much better return is available for that risk level or less, or how much better risk is available for that expected return or more. Doing this will require computing DAX measures, which will complicate the data model.

Apart from these kpi cards, we still need to decide on the title of the page as well as some relevant info to put at the top. For now i do not have a clear picture of what to put. Maybe the ID of the portfolio, the dates of the prices used, and the name of the model used "Standard Markowtiz".

##### Middle - "The Hero Visuals"

The hero visuals of this 1st page will consist of the treemap to the left showing the weights of the currently selected porfolio, as well as the scatter plot showing the efficient frontier to its right.

The treemap will show percentages as well as the ticker names of each of the stocks. The scatter plot will show in the x-axis the risk, in the y-axis the expected return, and it will have a colorbar to the left to identify the value of the sharpe ratio with heat coloring. Now, a line showing the approximate form of the efficient frontier should be plotted.

##### Bottom - "The Granular Detail"

Pending. I do not know what to add here.

##### Margins - "Navigation & Filtering"

Here i need to add the three slicer buttons to select the optimal portfolios. I also must add an option to find for the best porfolio for a given level of risk or return that the user can input. When the user inputs those values, the best porfolio for those metrics should be automatically choosen. I also should add a slicer button that redirects to the 2nd page.

On the placements of these buttons and fields, i think that the best is to leave to the left a rectangular section where these buttons can be selected. In a way the dahsboard will look like:

a____________________________________
|       |       (The KPI cards)     |
| Filte-|___________________________|
| ring  |                           |
|       |       The visuals         |
|       |                           |
|       |                           |
|       |                           |
|       |                           |
|       |                           |
a____________________________________
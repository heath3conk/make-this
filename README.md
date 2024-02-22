# Capstone project

## Problem statement
There are (at least) two general problems with using machine learning to solve problems.
1. Finding the "right" model for the problem at hand.
2. Understanding how the results can or should be used, for example identifying limitations, underlying 
    assumptions and potentially suspect applications.

AWS markets "a range of AutoML solutions for all levels of expertise"<sup>1</sup> and promises full
transparency into how their model was created and what's in it. H2O is an open-source tool that 
reads in data, produces a leaderboard of its best models and can also generate a number of charts and 
graphs to show its model's scores, variable importance, correlation of the models' predictions, etc.

From a learning perspective, my goal is to build a logical framework for choosing an appropriate ML model
based on the dataset provided and produce charts and evaluation metrics that are meaningful and useful to a non-technical audience.

I do not aim to reproduce AWS' AutoML or H2O results. I will create an interface where a user
will link data, interactively describe the problem they're trying to solve and then provide results 
with additional context so they can use the outcomes more effectively.


## Methodology
Write code that:
1. Takes in data
2. Does some EDA stuff<sup>*</sup> with it
3. Figures out/confirms with user what target column(s)
4. Based on the target, figures out/confirms with the user what type of problem this is
5. Identifies some models that are likely to work for that type of problem
6. Runs models & generates ranked results
7. Evaluates the results
8. Returns some stuff<sup>*</sup> to the user

<sup>*</sup>what exact stuff TBD

## Technical notes
### Installing requirements
- From the root of this repo, run `conda deactivate` to get out of any of your existing conda environments
- Hopefully, you're running zsh with a theme that shows your active conda environment - yes?
- Run `conda env create -f env.yml`

## References
1. [AWS AutoML Solutions](https://aws.amazon.com/machine-learning/automl/): Built-in AutoML across the AWS ML stack
2. [h2o.ai documentation](https://h2o.ai/platform/ai-cloud/make/h2o/)
3. [python H2O docs](https://docs.h2o.ai/h2o/latest-stable/h2o-py/docs/intro.html#what-is-h2o)
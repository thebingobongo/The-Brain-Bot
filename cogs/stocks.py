import asyncio
import io
import os
from collections import defaultdict
from pprint import pprint
from typing import List, Union
from urllib.parse import urlencode

import discord
import matplotlib.pyplot as plt
import numpy as np
import requests
import seaborn as sns
from colorthief import ColorThief
from databaselayer import *
from discord.ext import commands
from dotenv import load_dotenv
from pydash import defaults, pick, values

load_dotenv()
token = os.getenv('IEXCLOUD_TOKEN')

sns.set(
    style="darkgrid",
    palette="Set2",
    rc={
        "figure.facecolor": "#2f3136",
        "axes.facecolor": "#36393f",
        "axes.edgecolor": "#565b65",
        "grid.color": "#565b65",
        "text.color": "white",
        "axes.labelcolor": "white",
        "xtick.color": "#565b65",
        "ytick.color": "#565b65",
        "xtick.labelcolor": "white",
        "ytick.labelcolor": "white",
        "xtick.bottom": True,
        "ytick.left": True,
        "savefig.dpi": 300,
        "axes.spines.right": False,
        "axes.spines.top": False,
    },
)

COLOR = 0x5F8B84


def make_chart(data):
    data = np.array([values(pick(x, ["average", "label", "minute", "date"])) for x in data])
    data = data[data[:, 0] != None]
    averages, labels, minutes, dates = data[:, 0], data[:, 1], data[:, 2], data[:, 3]

    fig = plt.figure(constrained_layout=True)
    ax = fig.add_subplot(111)
    ax.plot(minutes, averages, label=labels)
    ax.set_xlabel("Time")
    ax.set_ylabel("Price [$]")
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))

    image = io.BytesIO()
    plt.savefig(image, format="png")
    plt.close()
    image.seek(0)
    return image


def make_request(
    ticker: Union[str, List[str]],
    endpoint: Union[str, List[str]],
    params: dict = {},
) -> dict:
    root = "https://cloud.iexapis.com/stable/stock/market/batch?"

    if type(ticker) == str:
        if len(ticker.split(",")) > 1:
            ticker = ticker.split(",")
        else:
            ticker = [ticker]

    params["symbols"] = ",".join(map(lambda x: x.lower(), ticker))
    params["types"] = ",".join(endpoint) if type(endpoint) == list else endpoint

    try:
        url = root + urlencode(defaults(params, {"token": token}), safe=",")
        res = requests.get(url)
        return res.json()
    except Exception as e:
        pprint(e)

    return {}


class Stocks(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.group(pass_context=True, aliases=["stocks", "s"])
    async def stock(self, ctx):
        if ctx.invoked_subcommand is None:
            msg = await ctx.send("Invalid use of stock command")
            await asyncio.sleep(2)
            await msg.delete()

    @stock.command(pass_context=True, aliases=["p"])
    async def price(self, ctx, ticker: str, *rest):
        await ctx.trigger_typing()

        tickers = [ticker] if len(rest) == 0 else [ticker, *rest]
        tickers = [*map(lambda x: x.lower(), tickers)]
        res = make_request(tickers, "quote")

        not_found, fields = [], []
        for x in tickers:
            x = x.upper()
            if not x in res:
                not_found.append(x)
                continue

            quote = res[x]["quote"]
            fields.append(pick(quote, ["symbol", "companyName", "latestPrice"]))

        if len(fields) == 0:
            return await ctx.send(f"Couldn't find data for {', '.join(not_found)} :(")

        embed = discord.Embed(color=COLOR)
        for field in fields:
            embed.add_field(
                name=f"${field['symbol'].upper()}",
                value=f":happybrain:{field['latestPrice']:.3f}",
                inline=True,
            )

        await ctx.send(embed=embed)

    @stock.command(pass_context=True, aliases=["i"])
    async def info(self, ctx, ticker: str):
        await ctx.trigger_typing()

        res = make_request(ticker, "company")

        try:
            info = res[ticker.upper()]["company"]
        except Exception as e:
            pprint(e)
            return await ctx.send(f"Couldn't find info on {ticker.upper()} :(")

        embed = discord.Embed(title=info["companyName"], description=info["description"])

        try:
            logo_url = make_request(ticker, "logo")[ticker.upper()]["logo"]["url"]
            embed.set_thumbnail(url=logo_url)

            logo = requests.get(logo_url)
            image = io.BytesIO(logo.content)
            color = ColorThief(image).get_color(quality=1)
            embed.color = discord.Color.from_rgb(*color)
        except Exception as e:
            pprint(e)
            pass

        for key in ["CEO", "sector", "country", "tags"]:
            value = info[key]
            if type(value) == list:
                value = ", ".join(value)
            embed.add_field(
                name=f"{key[0].upper()}{key[1:]}",
                value=value,
                inline=True,
            )

        await ctx.send(embed=embed)

    @stock.command(pass_context=True, aliases=["c"])
    async def chart(self, ctx, ticker: str):
        await ctx.trigger_typing()

        res = make_request(ticker, "intraday-prices")

        try:
            data = res[ticker.upper()]["intraday-prices"]
            chart = make_chart(data)
        except Exception as e:
            pprint(e)
            return await ctx.send("Something went wrong while making the chart :(")

        embed = discord.Embed(
            title=f"Trading history of ${ticker.upper()} on {data[0]['date']}",
            color=COLOR,
        )
        file = discord.File(chart, filename="chart.png")
        embed.set_image(url="attachment://chart.png")
        await ctx.send(file=file, embed=embed)

    @stock.command(pass_context=True, aliases=["b"])
    async def buy(self, ctx, ticker: str, amount: int):
        if amount <= 0:
            return

        await ctx.trigger_typing()

        res = make_request(ticker, "quote")

        try:
            quote = res[ticker.upper()]["quote"]
            price = float(quote["latestPrice"])

            if price <= 0:
                raise Exception("The stock market has collapsed. Please seek immediate shelter.")
        except Exception as e:
            pprint(e)
            return await ctx.send(f"Something went wrong buying shares of {ticker.upper()} :(")

        cost = price * amount
        if not hasEnough(ctx.author.id, cost):
            return await ctx.send("You're too poor to do that. Come back when you have the cash.")

        subBal(ctx.author.id, cost)
        addStocks(ctx.author.id, ticker, amount, price)

        await ctx.send(
            f"You bought {amount:d} share{'' if amount == 1 else 's'} of ${ticker.upper()} for {cost:.1f} Brain Cells."
        )

    @stock.command(pass_context=True, aliases=["s"])
    async def sell(self, ctx, ticker: str, amount: int):
        if amount <= 0:
            return

        await ctx.trigger_typing()

        if not hasStocks(ctx.author.id, ticker, amount):
            return await ctx.send(
                f"You don't have {amount:d} shares of ${ticker.upper()}, peasant."
            )

        res = make_request(ticker, "quote")

        try:
            quote = res[ticker.upper()]["quote"]
            price = float(quote["latestPrice"])
        except Exception as e:
            return await ctx.send(f"Couldn't get the price of ${ticker.upper()} :(")

        cash = price * amount
        removeStocks(ctx.author.id, ticker, amount)
        addBal(ctx.author.id, cash)

        await ctx.send(
            f"You sold {amount:d} share{'' if amount == 1 else 's'} of ${ticker.upper()} for {cash:.1f} Brain Cells."
        )

    @stock.command(pass_context=True)
    async def portfolio(self, ctx):
        await ctx.trigger_typing()

        stocks = getStocks(ctx.author.id)

        data = defaultdict(lambda: [])
        for stock in stocks:
            _, ticker, price, shares, timestamp = stock
            data[ticker.upper()].append([price, shares, timestamp])
        data = dict(data)

        if len(data.keys()) == 0:
            return await ctx.send("You got nothing to your name, poor boy.")

        quotes = make_request([*data.keys()], "quote")

        embed = discord.Embed(title=f"{ctx.author.name}'s portfolio", color=COLOR)
        for ticker, values in data.items():
            total_shares = sum([x[1] for x in values])

            try:
                quote = quotes[ticker.upper()]["quote"]
                price = quote["latestPrice"]
                # If shares bought at diff prices, compute the average change
                old_cash = sum([x[0] * x[1] for x in values])
                new_cash = price * total_shares
                change = (new_cash - old_cash) / old_cash * 100
            except:
                price = 0
                change = 0

            embed.add_field(name=ticker.upper(), value=f"\nShares: {total_shares}", inline=True)
            embed.add_field(
                name=f":happybrain:{(price * total_shares):.1f}",
                value=f"```diff\n{'+' if change > 0 else ''}{change:.2f}%\n```",
                inline=True,
            )
            embed.add_field(name="\u200b", value="\u200b", inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Stocks(bot))
